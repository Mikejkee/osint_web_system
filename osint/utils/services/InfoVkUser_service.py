from utils.services.my_service.Tele_parse import InfoVkUser
from utils.services.telegram_sessions.telegram_client import client_start
from time import time


"""
    "service_name": "Info Vk User",
    "input_parameters": "[!vk-id]",
    "Description": "InfoVkUser Parser info INPUT(vk-id), OUTPUT(vk-fio, vk-University, vk-residential_address)", 
"""


def main(input_parameters):
    start_time = time()
    client = client_start()
    with client:
        output_data = client.loop.run_until_complete(InfoVkUser(client, input_parameters['vk-id']))
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "vk-id",
                "data": input_parameters['vk-id']
            },
        ],
        'service_info': {
            "service_name": "InfoVkUser",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
