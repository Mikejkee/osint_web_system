from utils.services.my_service.Tele_parse import GetContact
from utils.services.telegram_sessions.telegram_client import client_start
from time import time


"""
    "service_name": "Get Contact",
    "input_parameters": "[!phones-number]",
    "Description": "GetContact Parser info INPUT(phones-number), OUTPUT(phones-owner)", 
"""


def main(input_parameters):
    start_time = time()
    client = client_start()
    with client:
        output_data = client.loop.run_until_complete(GetContact(client, input_parameters['phones-number']))
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "phones-number",
                "data": input_parameters['phones-number']
            },
        ],
        'service_info': {
            "service_name": "GetContact",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
