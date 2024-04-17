from utils.services.my_service.OSINT import Tutnaidut
from time import time

"""
    "service_name": "Tutnaidut",
    "input_parameters": "[!vk-id]",
    "Description": "Tutnaidut Parser info INPUT(ID), OUTPUT(Имя, пол, дата рождения, город, фото)", 
"""


def main(input_parameters):
    start_time = time()
    account_id = input_parameters['vk-id']
    profile = Tutnaidut(account_id)
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
            "service_name": "Tutnaidut",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data
    }
    return return_dic
