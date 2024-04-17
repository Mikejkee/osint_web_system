from utils.services.my_service.OSINT import Vk_photo
from time import time

"""
    "service_name": "VKPhoto",
    "input_parameters": "[!vk-id]",
    "Description": "VKPhoto Parser info INPUT(ID), OUTPUT(Имя, дата рождения, город)", 
"""


def main(input_parameters):
    start_time = time()
    account_id = input_parameters['vk-id']
    profile = Vk_photo(account_id)
    profile.search()
    output_data = profile.get_info()
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "vk-id",
                "data": account_id
            },
        ],
        'service_info': {
            "service_name": "VKPhoto",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data
    }
    return return_dic
