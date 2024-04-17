from utils.services.my_service.Tele_parse import VKUserInfo
from utils.services.telegram_sessions.telegram_client import client_start
from time import time

"""
    "service_name": "VKUserInfo",
    "input_parameters": "[!vk-id]",
    "Description": "VKUserinfo Parser info INPUT(URL), OUTPUT(имя, фамилия, аватар, город, страна, последнее посещение, платформа, дата регитсрации, домен, видимость страницы)", 
"""


def main(input_parameters):
    start_time = time()
    vk_id = input_parameters['vk-id']
    client = client_start()
    with client:
        output_data = client.loop.run_until_complete(VKUserInfo(client, vk_id))
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "vk-id",
                "data": vk_id
            },
        ],
        'service_info': {
            "service_name": "VKUserInfo",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
