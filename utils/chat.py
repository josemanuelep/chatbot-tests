
import requests
import json
import logging
import types
import pandas as pd

BASE_URI = 'https://api.vozy.ai/v2/chat/'

HEADERS = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhYdGVwY3ZLQjVBQzQxQ1JnbzZjViJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLnZvenkuYWkvIiwic3ViIjoiYXV0aDB8NjE5NTUzM2FjMGQyODQwMDcwNWY5MWIwIiwiYXVkIjpbImh0dHBzOi8vYXBpLnZvenkuYWkvYXV0aCIsImh0dHBzOi8vdm96eS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjQ0NTE2NTI2LCJleHAiOjE2NDQ2MDI5MjYsImF6cCI6IjhzRWNIbkpHaERmc2k2QnpXTDdqNHRQazlmNjJQdUlvIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsIm9yZ19pZCI6Im9yZ19nUVA4aGRJYU4xeTR0RTI2In0.SQn5CXwHBNQuIO7WPCKyvImv8TKbR38LrkLeNnsFvkdiJJ-tNze5vyGsEhw_8DoTHlBbPFbjDKQjAFgNKJFo2_nvDDWDX2be9sk_g0qWBAvOusaCl2QC_oMW_OhucmY2rhc3cD7AX3szf38J_urlwRYFq0LIXTTPUDfXe46Mfba6Mul1FRB4SiH83kozKwU8DhSS-6p97MxperaUyr5bX4pbz9Bi2fgtqA0IYPdQKTwKWPx572XQReMONWivzmIL0GT-HFHfQ6cZB6urDwj_h2ZznPYKqomAvTZCTANp7eTgzRbqKpgXzJYaiZU8YDSOtfq3Z4SkugsEi8E9nkExkA',
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


def init_chat_with_lili(identificator, url):

    payload = json.dumps({
        "from": identificator,
        "body": "Iniciar conversacion"})

    requests.request(
        "POST", url, headers=HEADERS, data=payload)


def load_file_with_data(file_name):
    df = pd.read_csv(file_name, delimiter=';')
    dict_data_test = df.to_dict('list')
    return dict_data_test


def get_chats_to_test(chats_to_test):

    list_of_node_names = list(chats_to_test.keys())
    first_node = list_of_node_names[0]
    len_of_node = len(chats_to_test[first_node])
    dict_with_conversation_flows = {}
    list_with_node_names_responses = []

    for x in range(len_of_node):
        dict_with_conversation_flows[x] = []

    for i, node in enumerate(list_of_node_names):

        # list_with_node_names_responses.append(chats_to_test[node].pop())

        for j, user_text in enumerate(chats_to_test[node]):

            list_to_add = dict_with_conversation_flows[j]
            list_to_add.append(user_text)
            dict_with_conversation_flows[j] = list_to_add

    chats = Chats(dict_with_conversation_flows,
                  list_with_node_names_responses, list_of_node_names)
    return chats

def log_newline(self, how_many_lines=1):
    self.removeHandler(self.console_handler)
    self.addHandler(self.blank_handler)
    for i in range(how_many_lines):
        self.info('')
    self.removeHandler(self.blank_handler)
    self.addHandler(self.console_handler)

def create_logger():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(fmt="%(name)s %(levelname)-8s: %(message)s"))

    blank_handler = logging.StreamHandler()
    blank_handler.setLevel(logging.DEBUG)
    blank_handler.setFormatter(logging.Formatter(fmt=''))

    logger = logging.getLogger('test-log')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    logger.console_handler = console_handler
    logger.blank_handler = blank_handler
    logger.newline = types.MethodType(log_newline, logger)

    return logger

    