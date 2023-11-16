from otree.api import *


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
    NUM_ROUNDS = 1
    DICTATOR_ROLE = 'Dictator'
    NO_DICTATOR_ROLE = 'No Dictator'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    amount_proposed = models.IntegerField()



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
        for player in group.get_players():
            
            player.messages = initial_messages
            player.tokens = 0
    ##fingpt
    pass


class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_group()[0].role)
    
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
        return ()
    
    pass



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [FirstWaitPage, MyPage, ResultsWaitPage, Results]
