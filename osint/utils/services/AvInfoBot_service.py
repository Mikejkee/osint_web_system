from utils.services.my_service.Tele_parse import AvinfoBotCar
from utils.services.telegram_sessions.telegram_client import client_start
from time import time

"""
    "service_name": "Avinfo Bot Car",
    "input_parameters": "[!car-number]",
    "Description": "AvinfoBotCar Parser info INPUT(car-number), OUTPUT(car info)", 
"""


def main(input_parameters):
    start_time = time()
    car_number = input_parameters['car-number']
    client = client_start()
    with client:
        output_data = client.loop.run_until_complete(AvinfoBotCar(client, car_number))
    return_dic = {
        'input_parameters':
            [
                {
                    "info_type": "emails-user_name",
                    "data": car_number
                },
            ],
        'service_info': {
            "service_name": "AvinfoBotCar",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
