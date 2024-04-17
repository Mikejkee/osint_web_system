from utils.services.my_service.OSINT import Propfr
from time import time

"""
    "service_name": "Propfr",
    "input_parameters": "[!nine-digits-snils]",
    "Description": "Propfr Parser info INPUT(nine-digits-snils), OUTPUT(СНИЛС)", 
"""


def main(input_parameters):
    start_time = time()
    nine_digits_snils = input_parameters['nine-digits-snils']
    profile = Propfr(nine_digits_snils)
    profile.search()
    output_data = profile.get_info()
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "vk-surname",
                "data": nine_digits_snils
            },
        ],
        'service_info': {
            "service_name": "Propfr",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
