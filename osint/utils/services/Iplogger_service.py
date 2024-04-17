from utils.services.my_service.OSINT import Iplogger
from time import time

"""
    "service_name": "Iplogger",
    "input_parameters": "[!IP_addresses-ip]",
    "Description": "Iplogger Parser info INPUT(IP), OUTPUT(Город, страна, порт, время, провайдер, регион, статус, координаты)", 
"""


def main(input_parameters):
    start_time = time()
    ip = input_parameters['IP_addresses-ip']
    profile = Iplogger(ip)
    profile.search()
    output_data = profile.get_info()
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "IP_addresses-ip",
                "data": ip
            },
        ],
        'service_info': {
            "service_name": "Iplogger",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
