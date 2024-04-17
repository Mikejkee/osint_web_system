import os
import re
import json
from pprint import pprint
import importlib.util

service_dir = './utils/services/'
# service_dir = './services/'
# chains_dir = './utils/search_chains/'
# chains_dir = './search_chains/'
about_parameters_dict = {
    "name": ["Имя", "text"],
    "surname": ["Фамилия", "text"],
    "patronymic": ["Отчество", "text"],
    "fio": ["ФИО", "text"],
    "nickname": ["Никнейм", "text"],
    "password": ["Пароль", "text"],
    "gender": ["Пол", "text"],
    "date_of_birth": ["Дата рождения", "text"],
    "place_of_birth": ["Место рождения", "text"],
    "registration_address": ["Адрес регистрации", "text"],
    "residence_address": ["Адрес проживания", "text"],
    "home_phone": ["Домашний телефон", "text"],
    "religion": ["Религия", "text"],
    "kindergartens-name": ["Название детского сада", "text"],
    "kindergartens-address": ["Адрес детского сада", "text"],
    "schools-name": ["Название школы", "text"],
    "schools-address": ["Адрес школы", "text"],
    "colleges-name": ["Название колледжа", "text"],
    "colleges-address": ["Адрес колледжа", "text"],
    "universities-name": ["Название университета", "text"],
    "universities-address": ["Адрес университета", "text"],
    "universities-start_date": ["Дата поступления в университет", "text"],
    "work-name": ["Название работы", "text"],
    "work-address": ["Адрес работы", "text"],
    "work-position": ["Должность", "text"],
    "work-number": ["Рабочий номер", "text"],
    "interests-name": ["Личный интерес", "text"],
    "incomes-name": ["Название зачисления на счет", "text"],
    "incomes-author": ["Автор зачисления", "text"],
    "incomes-amount": ["Сумма зачисления", "text"],
    "incomes-comment": ["Комментарий к зачислению", "text"],
    "expenses-name": ["Название вывода с счета", "text"],
    "expenses-receiver": ["Получатель вывода", "text"],
    "expenses-amount": ["Сумма вывода", "text"],
    "expenses-comment": ["Комментарий к выводу", "text"],
    "bank_accounts-name": ["Название банковского счета", "text"],
    "bank_accounts-number": ["Номер банковского счета", "text"],
    "bank_accounts-address": ["Адрес банка", "text"],
    "bank_accounts-comment": ["Комментарий к банковскому счету", "text"],
    "electronic_wallets-name": ["Название электронного счета", "text"],
    "electronic_wallets-number": ["Номер электронного счета", "text"],
    "electronic_wallets-account_type": ["Тип электронного счета", "text"],
    "electronic_wallets-comment": ["Комментарий к электронному счету", "text"],
    "estate-name": ["Название собственности", "text"],
    "estate-type": ["Тип собственности", "text"],
    "estate-comment": ["Комментарий к собственности", "text"],
    "car-number": ["Номер машины", "text"],
    "car-subject": ["Субъект РФ машины", "text"],
    "car-date_appeal": ["Дата обращения к машине", "text"],
    "car-owner": ["Владелец машины", "text"],
    "car-body_number": ["Номер кузова машины", "text"],
    "car-VIN": ["VIN машины", "text"],
    "car-category": ["Категория машины", "text"],
    "car-color": ["Цвет машины", "text"],
    "car-diagnostic card_number": ["Номер диагностической карты машины", "text"],
    "car-engine_number": ["Номер двигателя машины", "text"],
    "car-engine_power": ["Мощность двигателя машины", "text"],
    "car-engine_volume": ["Объем двигателя машины", "text"],
    "car-model": ["Модель машины", "text"],
    "car-count_owners": ["Количество собственников машины", "text"],
    "car-period_own": ["Период владения машиной", "text"],
    "car-type": ["Тип машины", "text"],
    "car-parking_session_number": ["Количество парковочных сессий", "text"],
    "car-validity_mot": ["Срок ТО машины", "text"],
    "car-year": ["Год выпуска машины", "text"],
    "car-other_information": ["Другая информация о машине", "text"],
    "twitter-name": ["Имя Twitter аккаунта", "text"],
    "twitter-type": ["Тип Twitter аккаунта", "text"],
    "twitter-id": ["ID Twitter аккаунта", "text"],
    "twitter-login": ["Login Twitter аккаута", "text"],
    "twitter-email": ["Почта Twitter аккаунта", "email"],
    "twitter-password": ["Пароль Twitter аккаунта", "text"],
    "twitter-followers_count": ["Количество подписчиков Twitter", "text"],
    "twitter-followings_count": ["Количество подписок Twitter", "text"],
    "twitter-registration_date": ["Дата регистрации Twitter аккаунта", "text"],
    "twitter-geo_position": ["Геопозиция Twitter аккаунта", "text"],
    "twitter-site": ["Сайт Twitter аккаунта", "text"],
    "twitter-description": ["Описание Twitter аккаунта", "text"],
    "twitter-comment": ["Комментарий к Twitter аккаунту", "text"],
	"facebook-name": ["Имя facebook аккаунта", "text"],
    "facebook-type": ["Тип facebook аккаунта", "text"],
    "facebook-id": ["ID facebook аккаунта", "text"],
    "facebook-login": ["Login facebook аккаута", "text"],
    "facebook-email": ["Почта facebook аккаунта", "email"],
    "facebook-password": ["Пароль facebook аккаунта", "text"],
    "facebook-followers_count": ["Количество подписчиков facebook", "text"],
    "facebook-followings_count": ["Количество подписок facebook", "text"],
    "facebook-registration_date": ["Дата регистрации facebook аккаунта", "text"],
    "facebook-geo_position": ["Геопозиция facebook аккаунта", "text"],
    "facebook-site": ["Сайт facebook аккаунта", "text"],
    "facebook-description": ["Описание facebook аккаунта", "text"],
    "facebook-comment": ["Комментарий к facebook аккаунту", "text"],
    "instagram-name": ["Имя Instagram аккаунта", "text"],
    "instagram-type": ["Тип Instagram аккаунта", "text"],
    "instagram-id": ["ID Instagram аккаунта", "text"],
    "instagram-email": ["Почта Instagram аккаунта", "email"],
    "instagram-assword": ["Пароль Instagram аккаунта", "text"],
    "instagram-followers_count": ["Количество подписчиков Instagram", "text"],
    "instagram-followings_count": ["Количество подписок Instagram", "text"],
    "instagram-site": ["Сайт Instagram аккаунта", "text"],
    "instagram-description": ["Описание Instagram аккаунта", "text"],
    "instagram-comment": ["Комментарий к Instagram аккаунту", "text"],
	"vk-fio": ["Имя Vk аккаунта", "text"],
	"vk-name": ["Имя Vk аккаунта", "text"],
    "vk-surname": ["Фамилия Vk аккаунта", "text"],
    "vk-patronymic": ["Отчество Vk аккаунта", "text"],
    "vk-date_of_birth": ["Дата рождения Vk аккаунта", "text"],
    "vk-place_of_birth": ["Место рождения Vk аккаунта", "text"],
    "vk-country": ["Страна Vk аккаунта", "text"],
    "vk-residential_address": ["Адрес прописки Vk аккаунта", "text"],
    "vk-gender": ["Пол Vk аккаунта", "text"],
    "vk-instagram": ["Instagram Vk аккаунта", "text"],
    "vk-twitter": ["Twitter Vk аккаунта", "text"],
    "vk-skype": ["Skype Vk аккаунта", "text"],
    "vk-facebook": ["Facebook Vk аккаунта", "text"],
    "vk-phone": ["Телефон Vk аккаунта", "text"],
    "vk-home_phone": ["Домашний телефон Vk аккаунта", "text"],
    "vk-job": ["Работа Vk аккаунта", "text"],
    "vk-school": ["Школа Vk аккаунта", "text"],
    "vk-University": ["Университет Vk аккаунта", "text"],
    "vk-type": ["Тип Vk аккаунта", "text"],
    "vk-id": ["ID Vk аккаунта", "text"],
    "vk-short_id": ["Короткое имя Vk аккаунта", "text"],
    "vk-login": ["Login Vk аккаунта", "text"],
    "vk-email": ["Почта Vk аккаунта", "email"],
    "vk-password": ["Пароль Vk аккаунта", "text"],
    "vk-domain": ["Сокращенная ссылка Vk аккаунта", "text"],
    "vk-page_status": ["Статус странциы Vk", "text"],
    "vk-last_seen": ["Последнее время посещения странциы Vk", "text"],
    "vk-platform": ["Платформа посещения странциы Vk", "text"],
    "vk-registered_date": ["Дата регистрации Vk аккаунта", "text"],
    "vk-followers_count": ["Количество подписчиков Vk", "text"],
    "vk-close_friends": ["Близкие друзья профиля Vk", "text"],
    "vk-friends_count": ["Количество друзей Vk", "text"],
    "vk-site": ["Сайт Vk аккаунта", "text"],
    "vk-description": ["Описание Vk аккаунта", "text"],
    "vk-comment": ["Комментарий к Vk аккаунту", "text"],
    "social_networks-type": ["Тип социальной сети", "text"],
    "social_networks-user_name": ["Имя в социальной сети", "text"],
    "social_networks-account_type": ["Тип аккаунта социальной сети", "text"],
    "social_networks-id": ["ID аккаунта социальной сети", "text"],
    "social_networks-login": ["Login аккаунта социальной сети", "text"],
    "social_networks-email": ["Почта аккаунта социальной сети", "email"],
    "social_networks-password": ["Пароль аккаунта социальной сети", "text"],
    "social_networks-description": ["Описани аккаунта социальной сети", "text"],
    "social_networks-comment": ["Комментарий к аккаунту социальной сети", "text"],
    "messengers-type": ["Тип мессенджера", "text"],
    "messengers-name": ["Имя в мессенджере", "text"],
    "messengers-account_type": ["Тип аккаунта мессенджера", "text"],
    "messengers-id": ["ID аккаунта мессенджера", "text"],
    "messengers-login": ["Login аккаунта мессенджера", "text"],
    "messengers-phone": ["Телефон аккаунта мессенджера", "text"],
    "messengers-password": ["Пароль аккаунта мессенджера", "text"],
    "messengers-comment": ["Комментарий к аккаунту мессенджера", "text"],
    "telegram-name": ["Имя аккаунта телеграмм", "text"],
    "telegram-account_type": ["Тип телеграмм аккаунта", "text"],
    "telegram-id": ["ID телеграмм аккаунта", "text"],
    "telegram-login": ["Login телеграмм аккаунта", "text"],
    "telegram-phone": ["Телефон телеграмм аккаунта", "text"],
    "telegram-password": ["Пароль телеграмм аккаунта", "text"],
    "telegram-comment": ["Комментарий к телеграмм аккаунту", "text"],
    "emails-user_name": ["Имя аккаунта почты", "text"],
    "emails-login": ["Login аккаунта почты", "text"],
    "emails-password": ["Пароль аккаунта почты", "text"],
    "emails-first_seen": ["Время первого упоминания аккаунта почты", "text"],
    "emails-last_seen": ["Время последнего упоминания аккаунта почты", "text"],
    "emails-credentials_leaked": ["Был ли взломан аккаунт почты", "text"],
    "emails-profiles": ["Профили к которым привязан аккаунт почты", "text"],
    "emails-domain": ["Домен аккаунта почты", "text"],
    "emails-comment": ["Комментарий к аккаунту почты", "text"],
    "game_platforms-name": ["Имя игрового аккаунта", "text"],
    "game_platforms-type": ["Тип игрового аккаунта", "text"],
    "game_platforms-id": ["ID игрового аккаунта", "text"],
    "game_platforms-login": ["Login игрового аккаунта", "text"],
    "game_platforms-email": ["Почта игрового аккаунта", "email"],
    "game_platforms-password": ["Пароль игрового аккаунта", "text"],
    "game_platforms-comment": ["Комментарий к игровому аккаунта", "text"],
    "forums-type": ["Тип форума", "text"],
    "forums-user_name": ["Имя форум аккаунта", "text"],
    "forums-account_type": ["Тип форум аккаунта", "text"],
    "forums-id": ["ID форум аккаунта", "text"],
    "forums-login": ["Login форум аккаунта", "text"],
    "forums-email": ["Почта форум аккаунта", "email"],
    "forums-password": ["Пароль форум аккаунта", "text"],
    "forums-comment": ["Комментарий к форум аккаунту", "text"],
    "MAC_addresses-name": ["Имя МАК адреса", "text"],
    "MAC_addresses-firm": ["Фирма устройства МАК адреса", "text"],
    "MAC_addresses-model": ["Модель устройства МАК адреса", "text"],
    "MAC_addresses-mac": ["МАК адрес", "text"],
    "MAC_addresses-comment": ["Комментарий к МАК адресу", "text"],
    "IP_addresses-name": ["Имя IP адреса", "text"],
    "IP_addresses-firm": ["Фирма устройства IP адреса", "text"],
    "IP_addresses-model": ["Модель устройства IP адреса", "text"],
    "IP_addresses-status": ["Статус IP адреса", "text"],
    "IP_addresses-city": ["Город IP адреса", "text"],
    "IP_addresses-country": ["Страна IP адреса", "text"],
    "IP_addresses-region": ["Регион IP адреса", "text"],
    "IP_addresses-port": ["Порт IP адреса", "text"],
    "IP_addresses-provider": ["ПровайдерIP адреса", "text"],
    "IP_addresses-position": ["Координаты IP адреса", "text"],
    "IP_addresses-time-zone": ["Часовой пояс IP адреса", "text"],
    "IP_addresses-ip": ["IP адрес", "text"],
    "IP_addresses-ASN": ["ASN IP адреса", "text"],
    "IP_addresses-Assignment": ["Назначение IP адреса", "text"],
    "IP_addresses-continent": ["Континент IP адреса", "text"],
    "IP_addresses-hostname": ["Имя хоста IP адреса", "text"],
    "IP_addresses-ISP": ["ISP IP адреса", "text"],
    "IP_addresses-postal_code": ["Индекс IP адреса", "text"],
    "IP_addresses-type": ["Тип IP адреса", "text"],
    "IP_addresses-service": ["Сервис IP адреса", "text"],
    "IP_addresses-comment": ["Комментарий к IP адресу", "text"],
    "URL_addresses-name": ["Имя URL адреса", "text"],
    "URL_addresses-firm": ["Фирма устройства URL адреса", "text"],
    "URL_addresses-model": ["Модель устройства URL адреса", "text"],
    "URL_addresses-status": ["Статус URL адреса", "text"],
    "URL_addresses-city": ["Город URL адреса", "text"],
    "URL_addresses-country": ["Страна URL адреса", "text"],
    "URL_addresses-region": ["Регион URL адреса", "text"],
    "URL_addresses-port": ["Порт URL адреса", "text"],
    "URL_addresses-provider": ["Провайдер URL адреса", "text"],
    "URL_addresses-position": ["Координаты URL адреса", "text"],
    "URL_addresses-creation_date": ["Дата создания URL адреса", "text"],
    "URL_addresses-time zone": ["Часовой пояс URL адреса", "text"],
    "URL_addresses-nserver": ["Список DNS-серверов URL адреса", "text"],
    "URL_addresses-registar_id": ["Идентификатор регистра URL адреса", "text"],
    "URL_addresses-url": ["URL адрес", "text"],
    "URL_addresses-ip": ["IP URL адреса", "text"],
    "URL_addresses-comment": ["Комментарий к URL аддресу", "text"],
    "URL_addresses-subdomains": ["Поддомены URL аддреса", "text"],
    "HWIDS-name": ["Имя HWID", "text"],
    "HWIDS-firm": ["Фирма устройства HWID", "text"],
    "HWIDS-model": ["Модель устройства HWID", "text"],
    "HWIDS-hwid": ["HWID", "text"],
    "HWIDS-comment": ["Комментарий к HWID", "text"],
    "DNSs-name": ["Имя DNS", "text"],
    "DNSs-firm": ["Фирма устройства DNS", "text"],
    "DNSs-model": ["Модель устройства DNS", "text"],
    "DNSs-dns": ["DNS", "text"],
    "DNSs-comment": ["Комментарий к DNS", "text"],
    "geo_tags-name": ["Имя геометки", "text"],
    "geo_tags-coordinates": ["Координаты геометки", "text"],
    "geo_tags-type": ["Тип геометки", "text"],
    "geo_tags-comment": ["Комментарий к геометке", "text"],
    "phones-type": ["Тип телефона", "text"],
    "phones-owner": ["Владелец телефона", "text"],
    "phones-model": ["Модель телефона", "text"],
    "phones-IMEI": ["IMEI телефона", "text"],
    "phones-number": ["Номер телефона", "text"],
    "phones-region": ["Регион номера телефона", "text"],
    "phones-time-zone": ["Часовой пояс номера телефона", "text"],
    "phones-number_operator_info": ["Информация об операторе номера телефона", "text"],
    "phones-sim_card": ["Номер сим карты телефона", "text"],
    "phones-comment": ["Комментарий к телефону", "text"],
    "passports-serial": ["Серия паспорта", "text"],
    "passports-number": ["Номер паспорта", "text"],
    "passports-departament": ["Подразделение выдавшее паспорт", "text"],
    "passports-departament_number": ["Номер подразделения выдавшего паспорт", "text"],
    "passports-issue_date": ["Дата выдачи паспорта", "text"],
    "international_passport-serial": ["Серия загран паспорта", "text"],
    "international_passport-number": ["Номер загран паспорта", "text"],
    "international_passport-departament": ["Подразделение выдавшее загран паспорт", "text"],
    "international_passport-departament_number": ["Номер подразделения выдавшего паспорт", "text"],
    "international_passport-issue_date": ["Дата выдачи загран паспорта", "text"],
    "driver_licenses-number": ["Номер водительских прав", "text"],
    "driver_licenses-departament": ["Подразделение выдавшее водительские права", "text"],
    "driver_licenses-categories": ["Категории водительских прав", "text"],
    "driver_licenses-issue_date": ["Дата выдачи водительских прав", "text"],
    "insurance_certificate-number": ["Номер страхового свидетельства", "text"],
    "nine-digits-snils": ["Первые 9 цифр страхового свидетельства", "text"],
    "insurance_certificate-issue_date": ["Дата выдачи страхового свидетельства", "text"],
    "policy-serial": ["Серия полиса", "text"],
    "policy-number": ["Номер полиса", "text"],
    "policy-departament": ["Подразделение выдавшее полис", "text"],
    "policy-issue_date": ["Дата выдачи полиса", "text"],
    "birth_certificate-number": ["Номер свидетельства о рождении", "text"],
    "birth_certificate-departament": ["Подразделение выдавшее свидетельство о рождении", "text"],
    "birth_certificate-act_number": ["Номер акта свидетельства о рождении", "text"],
    "birth_certificate-issue_date": ["Дата выдачи свидетельства о рождении", "text"],
    "military_id-number": ["Номер военного билета", "text"],
    "military_id-departament": ["Поздравление выдавшее военный билет", "text"],
    "military_id-issue_date": ["Дата выдачи военного билета", "text"],
    "employment_history-number": ["Номер трудовой книги", "text"],
    "employment_history-departament": ["Подразделение выдавшее трудовую книгу", "text"],
    "employment_history-issue_date": ["Дата выдачи трудовой книги", "text"],
    "education_documents-number": ["Номер документа об образовании", "text"],
    "education_documents-departament": ["Подразделение выдавшее документ об образовании", "text"],
    "education_documents-issue_date": ["Дата выдачи документа об образовании", "text"],
    "ITN": ["ИНН", "text"],
    "PSRNSP-number": ["Номер ОГРНИП", "text"],
    "PSRNSP-start_date": ["Дата присвоения ОГРНИП", "text"],
    "PSRNSP-end_date": ["Дата прекращения ОГРНИП", "text"],
	"avito-ad_url": ["Ссылка на объявление авито", "text"],
    "photo-path": ["Путь к фотографии", "file"],
    "photo-timestamp": ["Время фотографирования", "text"],
    "photo-coordinates": ["Координаты фотографии", "text"],
    "photo-divice_type": ["Координаты фотографии", "text"],
    "photo-comment": ["Комментарий к фотографии", "text"],
}

# TODO: Запуск create_service_info перед запуском системы, чтобы сформировать services_info.json


def service_list():
    # Возвращает список всех сервисов в папке
    return list(filter(lambda x: x.endswith('_service.py'), os.listdir(service_dir)))


def chains_list():
    # Возвращает список всех цепочек в папке
    return list(filter(lambda x: x.endswith('_chain.py'), os.listdir(chains_dir)))


def service_info_parser():
    service_list_info = []

    # Проходим по всем сервисам в папке, парсим их описание и создаем service_info.json
    for service_file in service_list():

        # Открываем файл на чтение
        with open("{}/{}".format(service_dir, service_file), 'r', encoding='utf-8') as file:
            code = file.read()

        # Вытаскиваем описание
        service_name = re.search('"service_name": "(.*?)"', code)[1]
        input_parameters = re.split(', ', re.search('"input_parameters": "\[(.*?)\]"', code)[1])

        # Формируем обязательные и не обязательные параметры
        edited_input_parameters = []
        for input_parameter in input_parameters:
            if input_parameter[0] == '!':
                edited_input_parameters.append({'importance': 1, 'value': input_parameter[1:]})
            else:
                edited_input_parameters.append({'importance': 0, 'value': input_parameter})

        description = re.search('"Description": "(.*?)"', code)[1]
        service_list_info.append({
            'service_file': service_file,
            'service_name': service_name,
            'input_parameters': edited_input_parameters,
            'description': description,
        })
    return service_list_info


def chain_info_parser():
    chain_list_info = []
    # Проходим по всем сервисам в папке, парсим их описание
    for chain_file in chains_list():

        # Открываем файл на чтение
        with open("{}/{}".format(chains_dir, chain_file), 'r', encoding='utf-8') as file:
            code = file.read()

        # Вытаскиваем описание
        chain_name = re.search('"chain_name": "(.*?)"', code)[1]
        input_parameters = re.split(', ', re.search('"input_parameters": "\[(.*?)\]"', code)[1])

        # Формируем обязательные и не обязательные параметры
        edited_input_parameters = []
        for input_parameter in input_parameters:
            if input_parameter[0] == '!':
                edited_input_parameters.append({'importance': 1, 'value': input_parameter[1:]})
            else:
                edited_input_parameters.append({'importance': 0, 'value': input_parameter})

        description = re.search('"Description": "(.*?)"', code)[1]
        chain_list_info.append({
            'chain_file': chain_file,
            'chain_name': chain_name,
            'input_parameters': edited_input_parameters,
            'description': description,
        })

    return chain_list_info


def create_service_info():
    service_info = service_info_parser()
    services_block = dict()
    parameters_block = dict()

    for service in service_info:
        parameters_info = dict()

        for parameter in service['input_parameters']:
            if parameter['importance'] == 1:
                parameters_info[parameter['value']] = {
                    'class': "form-control",
                    'about': about_parameters_dict[parameter['value']][0],
                    'type': about_parameters_dict[parameter['value']][1],
                    'onchange': "checkSearchParams(this.parentNode.parentNode)",
                }
            else:
                parameters_info[parameter['value']] = {
                    'class': "form-control",
                    'about': about_parameters_dict[parameter['value']][0],
                    'type': about_parameters_dict[parameter['value']][1],
                    'onchange': "",
                }
            try:
                parameters_block[about_parameters_dict[parameter['value']][0]].append(service['service_name'])
            except KeyError:
                parameters_block[about_parameters_dict[parameter['value']][0]] = list()
                parameters_block[about_parameters_dict[parameter['value']][0]].append(service['service_name'])

        services_block[service['service_name']] = dict(description=service['description'],
                                                       input_parameters=parameters_info)

    output_info = dict(parameters_block=parameters_block, service_info=services_block)
    with open('services_info.json', 'w+') as file:
        json.dump(output_info, file, sort_keys=False, ensure_ascii=False,)
    pprint(output_info)


def create_chain_info():
    chain_info = chain_info_parser()
    chains_block = dict()
    parameters_block = dict()

    for chain in chain_info:
        parameters_info = dict()
        for parameter in chain['input_parameters']:
            if parameter['importance'] == 1:
                parameters_info[parameter['value']] = {
                    'class': "form-control",
                    'about': about_parameters_dict[parameter['value']][0],
                    'type': about_parameters_dict[parameter['value']][1],
                    'onchange': "checkSearchParams(this.parentNode.parentNode)",
                }
            else:
                parameters_info[parameter['value']] = {
                    'class': "form-control",
                    'about': about_parameters_dict[parameter['value']][0],
                    'type': about_parameters_dict[parameter['value']][1],
                    'onchange': "",
                }
            try:
                parameters_block[about_parameters_dict[parameter['value']][0]].append(chain['chain_name'])
            except KeyError:
                parameters_block[about_parameters_dict[parameter['value']][0]] = list()
                parameters_block[about_parameters_dict[parameter['value']][0]].append(chain['chain_name'])

        chains_block[chain['chain_name']] = dict(description=chain['description'],
                                                 input_parameters=parameters_info)

    output_info = dict(parameters_block=parameters_block, chain_info=chains_block)
    with open('chains_info.json', 'w+') as file:
        json.dump(output_info, file, sort_keys=False, ensure_ascii=False,)
    pprint(output_info)


def get_service_functions(search_type, service_name, input_parameters):
    service_file = ""

    # # Либо сервис, либо цепочка
    # if search_type == 'service':
    for service in service_info_parser():
        if service['service_name'] == service_name:
            service_file = service['service_file']
    file_path = service_dir + service_file
    # elif search_type == 'chain':
    #     for chain in chain_info_parser():
    #         if chain['chain_name'] == service_name:
    #             service_file = chain['chain_file']
    #     file_path = chains_dir + service_file

    module_name = service_file[:-3]

    print(file_path)
    print(module_name)

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.main(input_parameters)

# create_service_info()
# create_chain_info()
# service_info_parser()
