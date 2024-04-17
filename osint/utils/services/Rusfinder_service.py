from utils.services.my_service.OSINT import Rusfinder
from time import time

"""
    "service_name": "Rusfinder",
    "input_parameters": "[!vk-surname, vk-name]",
    "Description": "Rusfinder Parser info INPUT(surname, name), OUTPUT(Имя, фамилия, дата рождения, место рожения, город, страна, skype, школа, университет, телефон, работа, vk_id,  фото)", 
"""


def main(input_parameters):
    start_time = time()
    surname = input_parameters['vk-surname']
    name = input_parameters['vk-name']
    profile = Rusfinder(surname, name)
    profile.search()
    output_data = profile.get_info()
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "vk-surname",
                "data": surname
            },
            {
                "info_type": "vk-name",
                "data": name
            },
        ],
        'service_info': {
            "service_name": "Rusfinder",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
