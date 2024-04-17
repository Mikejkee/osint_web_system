from utils.services.my_service.Tele_parse import Mailsearch
from utils.services.telegram_sessions.telegram_client import client_start
from time import time

"""
    "service_name": "Mailsearch",
    "input_parameters": "[!emails-user_name]",
    "Description": "Mailsearch Parser info INPUT(URL), OUTPUT(пароли)", 
"""


def main(input_parameters):
    start_time = time()
    mail = input_parameters['emails-user_name']
    client = client_start()
    with client:
        output_data = client.loop.run_until_complete(Mailsearch(client, mail))
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "emails-user_name",
                "data": mail
            },
        ],
        'service_info': {
            "service_name": "Mailsearch",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
