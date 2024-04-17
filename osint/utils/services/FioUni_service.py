from utils.services.my_service.Tele_parse import FindNameVk
from utils.services.telegram_sessions.telegram_client import client_start
from time import time


"""
    "service_name": "Fio Uni",
    "input_parameters": "[!fio, !universities-name]",
    "Description": "Fio Uni info INPUT(fio, universities-name), OUTPUT(universities-start_date)", 
"""

def main(input_parameters):
    start_time = time()
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "fio",
                "data": input_parameters['fio']
            },  
			{
                "info_type": "universities-name",
                "data": input_parameters['universities-name']
            },
        ],
        'service_info': {
            "service_name": "FioUni",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': {'universities-start_date': '1 ноября 2020'},
    }
    return return_dic
