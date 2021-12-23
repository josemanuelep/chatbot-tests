from json import dumps
from os import setregid
from uuid import uuid4
from pprint import pprint
import requests
import json
from assertpy import assert_that
import pandas as pd
from datetime import datetime
import time

agent = "e140ccbd-acb2-4e80-b3ae-f098372ac4d9"

url = " https://api.vozy.ai/v2/chat/"+agent


headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhYdGVwY3ZLQjVBQzQxQ1JnbzZjViJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLnZvenkuYWkvIiwic3ViIjoiYXV0aDB8NjE5NTUzM2FjMGQyODQwMDcwNWY5MWIwIiwiYXVkIjpbImh0dHBzOi8vYXBpLnZvenkuYWkvYXV0aCIsImh0dHBzOi8vdm96eS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjQwMjA3MjI4LCJleHAiOjE2NDAyOTM2MjgsImF6cCI6IjhzRWNIbkpHaERmc2k2QnpXTDdqNHRQazlmNjJQdUlvIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsIm9yZ19pZCI6Im9yZ19nUVA4aGRJYU4xeTR0RTI2In0.j2plo6evWdhMza7JRoSr9UGqgYGe3csgwm_5nfDNuTYJLEkFZeNBcJw3lKptmSPqTSXxz4v1lF8cezQIMVvWNFxqxQHog6SESwPAHMPMXlX2aJr2g7qFx2YGGit96fEW7Pi0J8tELRnSbsEe-a8BZ6nRHL3tIvASTxU7ijdRamnhEmiTkzwBNz-D8AxkdI79XdxzLpUGJFIowfN19cAkYEaBPlaxoGvHxXQ-uVmLVbAud_64gz-B6RcnN2bzPGIQGtDqH1kjgcOMuCjXk05ouhyLwm0CPWykPZdjQ73xtFxeIV8QfWxpO2za4gp16H9CD_F791kImTnRF4c7MiVPJweyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhYdGVwY3ZLQjVBQzQxQ1JnbzZjViJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLnZvenkuYWkvIiwic3ViIjoiYXV0aDB8NjE5NTUzM2FjMGQyODQwMDcwNWY5MWIwIiwiYXVkIjpbImh0dHBzOi8vYXBpLnZvenkuYWkvYXV0aCIsImh0dHBzOi8vdm96eS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjQwMjA3MjI4LCJleHAiOjE2NDAyOTM2MjgsImF6cCI6IjhzRWNIbkpHaERmc2k2QnpXTDdqNHRQazlmNjJQdUlvIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsIm9yZ19pZCI6Im9yZ19nUVA4aGRJYU4xeTR0RTI2In0.j2plo6evWdhMza7JRoSr9UGqgYGe3csgwm_5nfDNuTYJLEkFZeNBcJw3lKptmSPqTSXxz4v1lF8cezQIMVvWNFxqxQHog6SESwPAHMPMXlX2aJr2g7qFx2YGGit96fEW7Pi0J8tELRnSbsEe-a8BZ6nRHL3tIvASTxU7ijdRamnhEmiTkzwBNz-D8AxkdI79XdxzLpUGJFIowfN19cAkYEaBPlaxoGvHxXQ-uVmLVbAud_64gz-B6RcnN2bzPGIQGtDqH1kjgcOMuCjXk05ouhyLwm0CPWykPZdjQ73xtFxeIV8QfWxpO2za4gp16H9CD_F791kImTnRF4c7MiVPJw',
    'Content-Type': 'application/json'
}


class Chats:
    def __init__(self, dict_chats, dict_lili_responses):
        self.dict_chats = dict_chats
        self.dict_lili_responses = dict_lili_responses

    def get_dict_chats(self):
        return self.dict_chats

    def get_dict_responses(self):
        return self.dict_lili_responses

    def __str__(self):
        return str(self.dict_chats)+str(self.dict_lili_responses)


def test_chat_with_lili():

    dic = load_file_with_data('flow1.csv')

    chats_to_test = get_chats_to_test(dic)

    for utterancce, list_of_posibble_responses in chats_to_test.get_dict_chats().items():

        now = datetime.now()
        identificator = now.strftime("%H:%M:%S")
        init_chat_with_lili(identificator)

        for index, item in enumerate(list_of_posibble_responses):
            payload = json.dumps({
                "from": identificator,
                "body": item})

            time.sleep(1.2)

            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print(response.text)
            assert_that(response.status_code).is_equal_to(requests.codes.ok)
            assert_that(response.json()['message']).is_not_empty()
            assert_that(response.json()['message']).is_equal_to_ignoring_case(chats_to_test.get_dict_responses()[index])


def init_chat_with_lili(identificator):
    payload = json.dumps({
        "from": identificator,
        "body": "Hola"})
    response = requests.request(
        "POST", url, headers=headers, data=payload)


def load_file_with_data(file_name):
    df = pd.read_csv(file_name, delimiter=';')
    dict_data_test = df.to_dict('list')
    return dict_data_test


def get_chats_to_test(chats_to_test):
    list_of_node_names = list(chats_to_test.keys())
    first_node = list_of_node_names[0]
    len_of_node = len(chats_to_test[first_node])-1
    dict_with_conversation_flows = {}
    dict_with_node_names_responses = []

    for x in range(len_of_node):
        dict_with_conversation_flows[x] = []

    for i, node in enumerate(list_of_node_names):
        dict_with_node_names_responses.append(chats_to_test[node].pop())
        for j, user_text in enumerate(chats_to_test[node]):
            list_to_add = dict_with_conversation_flows[j]
            list_to_add.append(user_text)
            dict_with_conversation_flows[j] = list_to_add
    chats = Chats(dict_with_conversation_flows, dict_with_node_names_responses)
    return chats



