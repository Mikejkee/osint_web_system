from utils.services.my_service.Tele_parse import Userbox
from utils.services.telegram_sessions.telegram_client import client_start
from time import time


"""
    "service_name": "Userbox",
    "input_parameters": "[vk-id, phones-number, IP_addresses-ip, instagram-id, twitter-id, facebook-id]",
    "Description": "Userbox Parser info INPUT(vk-id, phones-number, IP_addresses-ip, instagram-id, twitter-id, facebook-id), OUTPUT(vk-fio, vk-short_id, vk-date_of_birth, vk-residential_address, vk-country, vk-email, vk-twitter, vk-instagram, vk-phone, phones-region, phones-number_operator_info, phones-time-zon, phones-owner, date_of_birth, telegram-id, emails-user_name, vk-id, password, IP_addresses-country, IP_addresses-city, IP_addresses-region, IP_addresses-hostname, IP_addresses-provider, IP_addresses-postal_code, IP_addresses-time-zone, IP_addresses-position)", 
"""



def main(input_parameters):
    start_time = time()
    client = client_start()
    with client:
        output_data = client.loop.run_until_complete(Userbox(client, input_parameters))
    input_info = list()
    for input_parameter in input_parameters:
        input_info.append(
            {
                "info_type": input_parameter,
                "data": input_parameters[input_parameter]
            },
        )
    return_dic = {
        'input_parameters': input_info,
        'service_info': {
            "service_name": "Userbox",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
