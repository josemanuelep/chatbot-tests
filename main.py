import json
from assertpy import assert_that
from datetime import datetime
import time
import requests
from utils.chat import BASE_URI, HEADERS, init_chat_with_lili, get_chats_to_test, load_file_with_data, create_logger
logger = create_logger()


def test_already_paid():

    agent = "e140ccbd-acb2-4e80-b3ae-f098372ac4d9"

    url = BASE_URI+agent

    test_file_name = 'csvs/debt_collection_flow2.csv'

    dic = load_file_with_data(test_file_name)

    chats_to_test = get_chats_to_test(dic)

    for i, list_of_posibble_responses in chats_to_test.get_dict_chats().items():

        now = datetime.now()
        identificator = now.strftime("%H:%M:%S")

        logger.newline()
        init_chat_with_lili(identificator, url)
        logger.info('----------------------  Flujo-'+str(i+1) +
                    '  ----------------------------------------------')
        logger.newline()

        for j, utterancce in enumerate(list_of_posibble_responses):

            payload = json.dumps({
                "from": identificator,
                "body": utterancce})

            time.sleep(1.6)

            response = requests.request(
                "POST", url, headers=HEADERS, data=payload)

            logger.info(utterancce)
            logger.newline()
            logger.info(str(response.json()['message']))

            assert_that(response.status_code).is_equal_to(
                requests.codes.ok)
            assert_that(response.json()['message']).is_not_empty()


test_already_paid()
