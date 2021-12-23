import pandas as pd


def load_file_with_data(file_name):  # Funtion to load data test in csv format
    df = pd.read_csv(file_name, delimiter=';')
    dict_data_test = df.to_dict('list')
    return dict_data_test


def get_dict_to_test(dict_with_test_data):

    list_of_node_names = list(dict_with_test_data.keys())
    first_node = list_of_node_names[0]
    len_of_node = len(dict_with_test_data[first_node])-1
    dict_with_conversation_flows = {}

    for x in range(len_of_node):
        dict_with_conversation_flows[x] = []

    for i, node in enumerate(list_of_node_names):
        dict_with_test_data[node].pop()
        for j, user_text in enumerate(dict_with_test_data[node]):
            list_to_add = dict_with_conversation_flows[j]
            list_to_add.append(user_text)
            dict_with_conversation_flows[j] = list_to_add
    return dict_with_conversation_flows
