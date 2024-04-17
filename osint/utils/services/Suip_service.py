from utils.services.my_service.OSINT import Suip
from time import time

"""
    "service_name": "Suip",
    "input_parameters": "[!URL_addresses-url]",
    "Description": "Suip Parser info INPUT(URL), OUTPUT(Поддомены)", 
"""


def main(input_parameters):
    start_time = time()
    url = input_parameters['URL_addresses-url']
    profile = Suip(url)
    profile.search()
    output_data = profile.get_info()
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "URL_addresses-url",
                "data": url
            },
        ],
        'service_info': {
            "service_name": "Suip",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
