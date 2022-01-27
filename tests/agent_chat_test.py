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


headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhYdGVwY3ZLQjVBQzQxQ1JnbzZjViJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLnZvenkuYWkvIiwic3ViIjoiYXV0aDB8NjE5NTUzM2FjMGQyODQwMDcwNWY5MWIwIiwiYXVkIjpbImh0dHBzOi8vYXBpLnZvenkuYWkvYXV0aCIsImh0dHBzOi8vdm96eS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjQzMjkzNjgyLCJleHAiOjE2NDMzODAwODIsImF6cCI6IjhzRWNIbkpHaERmc2k2QnpXTDdqNHRQazlmNjJQdUlvIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsIm9yZ19pZCI6Im9yZ19nUVA4aGRJYU4xeTR0RTI2In0.IiQUCKcp8vprtl7bbnZKSdCI4_4sE63DkVh4k5MrpIfSCrKkkGUaD1wWy-1iMfHqLxozPlcNQ3QMQV3kclPr-UQ4_NA9MdDvlckeRCxwPbN_c57Pfewe0rhCh3_-T5KwtTV_bxXgbHBWoqpNc69GjG6pGztB6gC3-4JDzzL45Xv4Gu7xYgZVpJbMiaVugUumn3EQymU55Z2nSQEi_91PeoxyqnItYavxDeuUUF3MWilpCqQbG8eS89jgG1H9Z81pB092D8DCONTAoABW_1NgTkiOZOaDau2jhnVHJO31NpWY9YzzXuRsvC5yK_bI-lSMp5q3Rv4AB3qAzAp2TQYd3A',
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


def test_already_paid():

    agent = "376147d1-d2f9-42aa-9be1-c280cf3f3ca6"

    url = " https://api.vozy.ai/v2/chat/"+agent

    test_file_name = 'QA_IPESOPE_final_testeo/gp_contact_no.csv'

    dic = load_file_with_data(test_file_name)

    chats_to_test = get_chats_to_test(dic)

    for i, list_of_posibble_responses in chats_to_test.get_dict_chats().items():

        now = datetime.now()
        identificator = now.strftime("%H:%M:%S")
        init_chat_with_lili(identificator, url)
        print('Flujo-'+str(i))
        print('')

        for j, utterancce in enumerate(list_of_posibble_responses):

            payload = json.dumps({
                "from": identificator,
                "body": utterancce})

            time.sleep(1.6)

            response = requests.request(
                "POST", url, headers=headers, data=payload)

            print('Human message: '+utterancce)
            print('Lili response: '+str(response.json()['message']))
            print('')

            assert_that(response.status_code).is_equal_to(
                requests.codes.ok)
            assert_that(response.json()['message']).is_not_empty()
            # assert_that(response.json()['message'].strip()).is_equal_to_ignoring_case(
            #     chats_to_test.get_list_responses()[j].strip())


def init_chat_with_lili(identificator, url):

    payload = json.dumps({
        "from": identificator,
        "body": "Iniciar conversacion"})

    requests.request(
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


test_already_paid()
