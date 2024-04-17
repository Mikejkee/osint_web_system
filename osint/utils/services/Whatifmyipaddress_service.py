from utils.services.my_service.OSINT import Whatifmyipaddress
from time import time

"""
    "service_name": "Whatifmyipaddress",
    "input_parameters": "[!IP_addresses-ip]",
    "Description": "Whatifmyipaddress Parser info INPUT(IP), OUTPUT(Город, страна, континент, ASN, ISP, индекс, провайдер, регион, тип, координаты, имя хоста, сервис)", 
"""


def main(input_parameters):
    start_time = time()
    ip = input_parameters['IP_addresses-ip']
    profile = Whatifmyipaddress(ip)
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
            "service_name": "Whatifmyipaddress",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
