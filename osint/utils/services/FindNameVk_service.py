from utils.services.my_service.Tele_parse import FindNameVk
from utils.services.telegram_sessions.telegram_client import client_start
from time import time


"""
    "service_name": "Find Name Vk",
    "input_parameters": "[!vk-id]",
    "Description": "FindNameVk Parser info INPUT(vk-id), OUTPUT(vk-fio, vk-registered_date)", 
"""

def main(input_parameters):
    start_time = time()
    client = client_start()
    with client:
        output_data = client.loop.run_until_complete(FindNameVk(client, input_parameters['vk-id']))
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "vk-id",
                "data": input_parameters['vk-id']
            },
        ],
        'service_info': {
            "service_name": "FindNameVk",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
