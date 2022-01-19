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
import csv

agent = "e140ccbd-acb2-4e80-b3ae-f098372ac4d9"

url = " https://api.vozy.ai/v2/chat/"+agent


headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhYdGVwY3ZLQjVBQzQxQ1JnbzZjViJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLnZvenkuYWkvIiwic3ViIjoiYXV0aDB8NjE5NTUzM2FjMGQyODQwMDcwNWY5MWIwIiwiYXVkIjpbImh0dHBzOi8vYXBpLnZvenkuYWkvYXV0aCIsImh0dHBzOi8vdm96eS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjQxOTMxMDk0LCJleHAiOjE2NDIwMTc0OTQsImF6cCI6IjhzRWNIbkpHaERmc2k2QnpXTDdqNHRQazlmNjJQdUlvIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsIm9yZ19pZCI6Im9yZ19nUVA4aGRJYU4xeTR0RTI2In0.lHgBIuG9NdPPHM65Pi4ODhM72VXLDzU2-OGPNPUVBcDX65mY-vlT3Dm9ONBLOGdgfh9u1LukVulSGC8EaBajuuA_hU4JqkQXXjOBdetRQfHH2oos6ILbdAxqBfXRZZ-p442Xu7MjtL_JZEZJWLVQr2k-r4aR5pKSRAlgO5KIANJejPEDTRuORVzEV1Iepf1PVI5lQG1ugezeuCNtfrXqH00bSndkCdR1I81xnTO2xDVKOAlNjONaxJe9FTUwJ_h3wOAbWDHDs2wSuwjz8oQ6jMU55j7a8oE68cyI4xv5W_4DCrptAYVJmORZvzojXY5zBLWC7F2J-q13MpxMDBdtSA',
    'Content-Type': 'application/json'
}


class Chats:
    def __init__(self, dict_chats, list_lili_responses, list_intents_names):
        self.dict_chats = dict_chats
        self.list_lili_responses = list_lili_responses
        self.list_intents_names = list_intents_names

    def get_dict_chats(self):
        return self.dict_chats

    def get_list_responses(self):
        return self.list_lili_responses

    def get_list_intents_names(self):
        return self.list_intents_names

    def __str__(self):
        return str(self.dict_chats)+'--'+str(self.list_lili_responses)+'--'+str(self.list_intents_names)


def test_chat_with_lili():

    test_file_name = 'debt_collection_flow1.csv'

    dic = load_file_with_data(test_file_name)

    chats_to_test = get_chats_to_test(dic)

    with open('results_'+test_file_name, 'w', encoding='UTF8') as f:

        writer = csv.writer(f)
        header = chats_to_test.get_list_intents_names()
        writer.writerow(header)

        for i, list_of_posibble_responses in chats_to_test.get_dict_chats().items():

            now = datetime.now()
            identificator = now.strftime("%H:%M:%S")
            init_chat_with_lili(identificator)
            print(list_of_posibble_responses)

            for j, utterancce in enumerate(list_of_posibble_responses):

                payload = json.dumps({
                    "from": identificator,
                    "body": utterancce})
                time.sleep(1.6)

                response = requests.request(
                    "POST", url, headers=headers, data=payload)
                
                response_of_lili = response.json()['message']
                # if response_of_lili.lower() == chats_to_test.get_list_responses()[j].lower():
                #     print('Human: '+utterancce, 'Lili: ' +
                #           response_of_lili.lower())
                list_of_posibble_responses.insert(j+1, 0)
                writer.writerow(list_of_posibble_responses)
                assert_that(response.status_code).is_equal_to(
                    requests.codes.ok)
                assert_that(response.json()['message']).is_not_empty()
                assert_that(response.json()['message']).is_equal_to_ignoring_case(chats_to_test.get_list_responses()[j])


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
    list_with_node_names_responses = []

    for x in range(len_of_node):
        dict_with_conversation_flows[x] = []

    for i, node in enumerate(list_of_node_names):

        list_with_node_names_responses.append(chats_to_test[node].pop())

        for j, user_text in enumerate(chats_to_test[node]):

            list_to_add = dict_with_conversation_flows[j]
            list_to_add.append(user_text)
            dict_with_conversation_flows[j] = list_to_add

    chats = Chats(dict_with_conversation_flows,
                  list_with_node_names_responses, list_of_node_names)
    return chats


test_chat_with_lili()
