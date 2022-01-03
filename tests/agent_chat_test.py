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
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhYdGVwY3ZLQjVBQzQxQ1JnbzZjViJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLnZvenkuYWkvIiwic3ViIjoiYXV0aDB8NjE5NTUzM2FjMGQyODQwMDcwNWY5MWIwIiwiYXVkIjpbImh0dHBzOi8vYXBpLnZvenkuYWkvYXV0aCIsImh0dHBzOi8vdm96eS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjQxMjIzNTY3LCJleHAiOjE2NDEzMDk5NjcsImF6cCI6IjhzRWNIbkpHaERmc2k2QnpXTDdqNHRQazlmNjJQdUlvIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsIm9yZ19pZCI6Im9yZ19nUVA4aGRJYU4xeTR0RTI2In0.l66OYfK_RP_MHNQCd7buC2Evo31XGX15RRNpEDFvetIr3AYVOlD144aDDyj-adcvBY8vsbajee-cEd2iuOfhbqf8h_1IRNNREC0ZT-CK-fKwKgESCSFAfECjscR6dEU45IB0wB992Ei0lzl0bPgjS-g5l85s6dnwXCrDx-4VIqa_-eNaBwutcxWLKnE7VRrH6oFdGvxUnoFf8WsdsbCBjfzfVtLydk-OTi9Z_qMFgdKxl1lP1H-qhTJcNPNeXIVuTi2EcLWa0npvvgk3JuijhFVc7rq1CEI-Ehhc9AdXhtxIlWL4E_wm6TRmKGW6SgOgxN9Jy5g2jGeVar6HRpm5mg',
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

    dic = load_file_with_data('debt_collection_flow1.csv')

    chats_to_test = get_chats_to_test(dic)

    for i, list_of_posibble_responses in chats_to_test.get_dict_chats().items():

        now = datetime.now()
        identificator = now.strftime("%H:%M:%S")
        init_chat_with_lili(identificator)

        for j, utterancce in enumerate(list_of_posibble_responses):
            payload = json.dumps({
                "from": identificator,
                "body": utterancce})

            time.sleep(1.5)

            response = requests.request(
                "POST", url, headers=headers, data=payload)

            print('Humano :', utterancce)
            print('Lili :', response.text)

            assert_that(response.status_code).is_equal_to(requests.codes.ok)
            assert_that(response.json()['message']).is_not_empty()
            # assert_that(response.json()['message']).is_equal_to_ignoring_case(chats_to_test.get_dict_responses()[index])


def init_chat_with_lili(identificator):
    payload = json.dumps({
        "from": identificator,
        "body": "Iniciar conversacion"})
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


test_chat_with_lili()
