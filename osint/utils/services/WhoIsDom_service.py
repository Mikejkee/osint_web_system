from utils.services.my_service.Tele_parse import WhoIsDom
from utils.services.telegram_sessions.telegram_client import client_start
from time import time

"""
    "service_name": "Whoisdom",
    "input_parameters": "[!URL_addresses-url]",
    "Description": "Whoisdom Parser info INPUT(URL), OUTPUT(ip, домены, список DNS-серверов, дата создания, )", 
"""


def main(input_parameters):
    start_time = time()
    domain = input_parameters['URL_addresses-url']
    client = client_start()
    with client:
        output_data = client.loop.run_until_complete(WhoIsDom(client, domain))
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "URL_addresses-url",
                "data": domain
            },
        ],
        'service_info': {
            "service_name": "Whoisdom",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
