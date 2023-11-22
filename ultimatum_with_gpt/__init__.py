from otree.api import *


#Configuracion del archivo csv: 
import csv
archivo_csv = 'config.csv'
datos = []
with open(archivo_csv, newline='') as csvfile:
    lector_csv = csv.DictReader(csvfile)
    for fila in lector_csv:
        datos.append(fila)

# Acceder a los valores
segments = int(datos[0]['segments'])
periods_per_segment = int(datos[0]['periods_per_segment'])
endowment = datos[0]['endowment']



#open ai and json
import json
from openai import OpenAI
client = OpenAI(api_key="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")

doc = """
Your app description
"""


initial_messages=[
            #{"role": "system", "content": "Eres un asistente eficiente y serio."},
#            {"role": "user", "content": "El orden de los factores no altera el producto?"},
#            {"role": "assistant", "content": "Exacto, el orden de los factores no altera el producto"},
            
        ]
messages=[
            {"role": "system", "content": "Eres un profesor."},
            {"role": "user", "content": "El orden de los factores no altera el producto?"},
            {"role": "assistant", "content": "Exacto, el orden de los factores no altera el producto"},
            
        ]

class C(BaseConstants):
    NAME_IN_URL = 'ultimatum_with_gpt'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = segments
    ENDOWMENT = endowment
    DICTATOR_ROLE = 'Sender'
    NO_DICTATOR_ROLE = 'Receiver'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    periodo = models.IntegerField(initial=0)
    endowment = models.IntegerField(initial=C.ENDOWMENT)

    amount_proposed = models.IntegerField()


    ##codigo para el historial:
    historial = models.LongStringField(initial="")
    _historial = models.StringField()

    @property
    def historial(self):
        _historial = self.field_maybe_none('_historial')
        if _historial is None:
            return []
        else:
            return json.loads(_historial)

    @historial.setter
    def historial(self, value):
        self._historial = json.dumps(value)


    ##codigo para el chat
    messages = models.LongStringField(initial="")
    _messages = models.StringField()
    tokens = models.IntegerField()
    @property
    def messages(self):
        _messages = self.field_maybe_none('_messages')
        if _messages is None:
            return []
        else:
            return json.loads(_messages)
    @messages.setter
    def messages(self, value):
        self._messages = json.dumps(value)
    pass


# PAGES

class FirstWaitPage(WaitPage):


    
    ##gpt
    @staticmethod
    def after_all_players_arrive(group: Group):
        ##periodos
        for p in group.get_players():
            p.periodo = 1

        ##gpt
        for player in group.get_players():
            
            player.messages = initial_messages
            player.tokens = 0
    ##fingpt
    pass


class MyPage(Page):
    
    endowment = C.ENDOWMENT

    @staticmethod
    def vars_for_template(player: Player):
        historial = []
        try:
            datos_en_rondas_previas = player.in_all_rounds()
            for i in range(len(datos_en_rondas_previas)):
                historial_de_periodo = datos_en_rondas_previas[i].historial
                for j in range(len(historial_de_periodo)):
                    historial.append(historial_de_periodo[j])
                pass
            

            
        except:
            print("sin historial")
            historial = []
        print("historial: ", historial)
        return dict(other_role=player.get_others_in_group()[0].role, historial = historial)
    
    @staticmethod
    def live_method(player, data):
        if data['type'] == 'propose':
            print("propose", data['offer'])
            proposals = []
            [other] = player.get_others_in_group()
            for p in [player, other]:
                amount_proposed = p.field_maybe_none('amount_proposed')
                if amount_proposed is not None:
                    proposals.append([p.id_in_group, amount_proposed])
            return {0: dict(proposals=proposals,offer=data['offer'])}



        #gpt
        if data['type'] == 'chat_gpt':
            mensajes = player.messages
            print(len(mensajes))
            if len(mensajes) == 0:
                mensajes = [{"role": "user", "content": data['message']}]
            else:
                mensajes.append({"role": "user", "content": data['message']})
            
            #player.messages = mensajes
            response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            #model="gpt-3.5-turbo",
            messages=mensajes,
            #temperature = 0 
            )
            #print(data['message'])
            
            #print(response.choices)
            final_response = response.choices[0].message.content
            #print(final_response)

            mensajes.append({"role": "assistant", "content": final_response})
            player.messages = mensajes
            #print("player messages: ",mensajes)
            #print(player.messages)
            #print(final_response)


            player.tokens = player.tokens + response.usage.total_tokens
            print("model: ", response.model)
            print("tokens usados: ", player.tokens)
            #data_to_sent = dict('type' : 'chat_gpt', message: final_response)
            data_to_sent = {'type': 'chat_gpt', 'message': final_response}
            return {player.id_in_group: data_to_sent}
            
            '''
            player.messages = mensajes
            print("player messages: ",mensajes)
            return {player.id_in_group: data['message']}
            '''
            
        #fin gpt

        if data['type'] == 'response':
            return {0: data}
        
        if data['type'] == 'sender_send':

            return {player.id_in_group: data, player.get_others_in_group()[0].id_in_group:data}
        
        if data['type'] == 'guardar_historial':
            segmento = data['segmento']
            periodo = data['periodo']
            puntos = data['puntos']
            nueva_entrada_historial = {'segmento':segmento, 'periodo': periodo,'puntos': puntos}
            historial = player.historial
            historial.append(nueva_entrada_historial)
            player.historial = historial
            print("historial de usuario ", player.id_in_group, ": ",player.historial)
            return {}
        return ()
    
    pass



class ResultsWaitPage(WaitPage):
    
    @staticmethod
    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            p.periodo = p.periodo +1

            
            
            #print("historial: "  ,p.historial)
    pass


class Results(Page):
    pass

#sequence = [InitPage]
sequence = [FirstWaitPage]
for i in range(periods_per_segment):
    sequence.append(MyPage)
    #sequence.append(Results)
    sequence.append(ResultsWaitPage)

#page_sequence = [FirstWaitPage, MyPage, ResultsWaitPage, Results]
page_sequence = sequence