from utils.services.my_service.OSINT import Vin01
from time import time

"""
    "service_name": "Vin01",
    "input_parameters": "[!car-number, !car-VIN]",
    "Description": "Vin01 Parser info INPUT(URL), OUTPUT(VIN, номер кузова, госномер, категория, цвет, номер ДК, номер двигателя, мощность двигателя, объем двигателя, модель, количество владельцев, период владения, тип машины, срок ТО, год выпуска)", 
"""


def main(input_parameters):
    start_time = time()
    car_number = input_parameters['car-number']
    car_VIN = input_parameters['car-VIN']
    profile = Vin01(car_number, car_VIN)
    profile.search()
    output_data = profile.get_info()
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "car-number",
                "data": car_number
            },
            {
                "info_type": "car-VIN",
                "data": car_VIN
            },
        ],
        'service_info': {
            "service_name": "Vin01",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
