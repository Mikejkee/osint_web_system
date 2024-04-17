from telethon.sync import TelegramClient
from telethon import connection
import json


proxy_ip = 'proxy.digitalresistance.dog'
proxy_port = 443
secret = ''


def client_start():
    # Загружаем инфу о сессиях
    # with open('./services/telegram_sessions/sessions_info.json', "r") as read_file:
    with open('./utils/services/telegram_sessions/sessions_info.json', "r") as read_file:
        sessions_info = json.load(read_file)

    # Загружаем номер последней используемой сессии
    # with open('./services/telegram_sessions/sessions_log.json', "r") as read_file:
    with open('./utils/services/telegram_sessions/sessions_log.json', "r") as read_file:
        last_session_number = json.load(read_file)

    # Находим номер сессии, которая реже использовалась:
    sessions_count = len(sessions_info)
    current_session_number = int(last_session_number) % sessions_count

    # Изменяем номер последней используемой сесии и логируем
    # with open('./services/telegram_sessions/sessions_log.json', "w+") as file:
    with open('./utils/services/telegram_sessions/sessions_log.json', "w+") as file:
        session_new_number = (current_session_number + 1) % sessions_count
        json.dump(session_new_number, file)
    print('Поменял номер сессии')

    # Открываем сессию
    client = TelegramClient(sessions_info[current_session_number]['session_name'],
                            sessions_info[current_session_number]['api_id'],
                            sessions_info[current_session_number]['api_hash'],
                            proxy=(proxy_ip, proxy_port, secret),
                            connection=connection.tcpmtproxy.ConnectionTcpMTProxyIntermediate).start()

    return client
