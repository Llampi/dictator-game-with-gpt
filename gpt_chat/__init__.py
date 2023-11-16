from otree.api import *
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
    NAME_IN_URL = 'gpt_chat'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):


    # crear el historial de mensajes
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



    chat = models.StringField()
    pass


# PAGES
class firstWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            player.chat = ""
            player.messages = initial_messages
            player.tokens = 0
    pass

class MyPage(Page):
    def live_method(player, data):
        mensajes = player.messages
        print(len(mensajes))
        if len(mensajes) == 0:
            mensajes = [{"role": "user", "content": data}]
        else:
            mensajes.append({"role": "user", "content": data})
        
        #player.messages = mensajes
        response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        #model="gpt-3.5-turbo",
        messages=mensajes,
        #temperature = 0 
        )
        #print(data)
        
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
        return {player.id_in_group: final_response}
        
        '''
        player.messages = mensajes
        print("player messages: ",mensajes)
        return {player.id_in_group: data}
        '''
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [firstWaitPage, MyPage, ResultsWaitPage, Results]
