from utils.services.my_service.OSINT import Urllogger
from time import time

"""
    "service_name": "Urllogger",
    "input_parameters": "[!URL_addresses-url]",
    "Description": "Urllogger Parser info INPUT(URL), OUTPUT(Город, ip, страна, порт, время, провайдер, регион, статус, координаты)", 
"""


def main(input_parameters):
    start_time = time()
    url = input_parameters['URL_addresses-url']
    profile = Urllogger(url)
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
            "service_name": "Urllogger",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
