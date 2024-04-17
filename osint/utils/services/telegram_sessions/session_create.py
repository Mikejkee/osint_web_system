from telethon.sync import TelegramClient
from telethon import connection
import json
import os

input_dict = [
    {
        'phone_number': '',
        'api_id': ,
        'api_hash': '',
        'session_name': '',
    },
    {
        'phone_number': '',
        'api_id': ,
        'api_hash': '',
        'session_name': '',
    },
]

proxy_ip = 'proxy.digitalresistance.dog'
proxy_port = 443
secret = ''

"""
    Example input format (для создания json и файлов сессий):
    input = [
        {
            'phone_number': 8989898988,
            'api_id': 1111111,
            'api_hash': 'fsdfdsihfdshfvjduigvdubd',
            'session_name': '@sess',
        },
        {
            'phone_number': 898989707070,
            'api_id': 439758458,
            'api_hash': 'fhsigfjbdaihdoigafsfhgduh',
            'session_name': '@sesssss',
        },
    ]    
"""
# TODO: Запуск из докера celery, чтобы сессии были под эту конкретную систему


def create_session(sessions_info):
    for session in sessions_info:
        TelegramClient(session['session_name'], session['api_id'], session['api_hash'],
                       proxy=(proxy_ip, proxy_port, secret),
                       connection=connection.tcpmtproxy.ConnectionTcpMTProxyIntermediate).start()
    with open('sessions_info.json', 'w+') as file:
        json.dump(sessions_info, file, sort_keys=False, ensure_ascii=False,)


# create_session(input_dict)
