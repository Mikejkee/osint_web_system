import os
import re
import requests
from telethon import events


def merge_two_dicts(x, y):
    """Объединение двух словарей без повторений."""
    z = x.copy()
    z.update(y)
    return z


def userbox_ip_parse(message):
    result_dict = dict()

    # Забираем инфу об ip
    try:
        result_dict['IP_addresses-country'] = re.search('Страна: `(.*?)`', message[0].text)[1]
    except TypeError:
        pass
    try:
        result_dict['IP_addresses-city'] = re.search('Город: `(.*?)`', message[0].text)[1]
    except TypeError:
        pass
    try:
        result_dict['IP_addresses-region'] = re.search('Регион: `(.*?)`', message[0].text)[1]
    except TypeError:
        pass
    try:
        result_dict['IP_addresses-hostname'] = re.search('Хост: `(.*?)`', message[0].text)[1]
    except TypeError:
        pass
    try:
        result_dict['IP_addresses-provider'] = re.search('Провайдер: `(.*?)`', message[0].text)[1]
    except TypeError:
        pass
    try:
        result_dict['IP_addresses-postal_code'] = re.search('Индекс: `(.*?)`', message[0].text)[1]
    except TypeError:
        pass
    try:
        result_dict['IP_addresses-time-zone'] = re.search('Часовой пояс: `(.*?)`', message[0].text)[1]
    except TypeError:
        pass
    try:
        result_dict['IP_addresses-position'] = re.search('Координаты: `(.*?)`', message[0].text)[1].split(',')
    except TypeError:
        pass

    return result_dict


def userbox_phone_parse(message):
    result_dict = dict()

    # Забираем инфу о телефоне
    try:
        result_dict['phones-region'] = re.search(r'\*\*Регион:\*\* (.*?)\n', message.text)[1]
    except TypeError:
        pass
    try:
        result_dict['phones-number_operator_info'] = re.search(r'\*\*Оператор:\*\* (.*?)\n', message.text)[1]
    except TypeError:
        pass
    try:
        result_dict['phones-time-zon'] = re.search(r'\*\*Часовой пояс:\*\* (.*?)\n', message.text)[1]
    except TypeError:
        pass

    owners = re.findall(r'ФИО:\*\* `(.*?)`', message.text, re.M)
    if len(owners) != 0:
        result_dict['fio'] = owners

    owners = re.findall(r"Имя:\*\*.*?['|`](\w*?)['|`].*?Фамилия:\*\*.*?['|`](\w*?)['|`]", message.text, re.M | re.S)
    if len(owners) != 0:
        list_owners = list()
        for owner in owners:
            list_owners.append("{} {}".format(owner[0], owner[1]))
        if 'fio' not in result_dict:
            result_dict['fio'] = list_owners
        else:
            result_dict['fio'].append(list_owners)
    try:
        result_dict['date_of_birth'] = re.search(r'\*\*Дата рождения:\*\* `(.*?)`', message.text)[1]
    except TypeError:
        pass
    try:
        result_dict['telegram-id'] = re.search(r'Telegram.*?User ID:\*\* (.*?)\n', message.text)[1]
    except TypeError:
        pass
    result_dict['emails-user_name'] = re.findall(r"Email:\*\*.*?['|`](\b.*?)['|`]", message.text)
    result_dict['vk-id'] = re.findall(r'vk.com/id(\d*)\)', message.text)
    result_dict['password'] = re.findall(r"Пароль:\*\*.*?['|`](.*)['|`]", message.text)

    return result_dict


def userbox_vk_parse(message):
    result_dict = dict()

    # Забираем инфу о вк
    owners = re.findall(r"Имя:\*\*.*?['|`](\w*?)['|`].*?Фамилия:\*\*.*?['|`](\w*?)['|`]", message.text, re.M | re.S)
    if len(owners) != 0:
        list_owners = list()
        for owner in owners:
            list_owners.append("{} {}".format(owner[0], owner[1]))
        result_dict['fio'] = list_owners
    result_dict['vk-short_id'] = re.findall(r"Screen name:\*\*.*?['|`](.*)['|`]", message.text)
    result_dict['vk-date_of_birth'] = re.findall(r"Дата рождения:\*\*.*?['|`](.*)['|`]", message.text)
    result_dict['vk-residential_address'] = re.findall(r"Город:\*\*.*?['|`](.*)['|`]", message.text)
    result_dict['vk-country'] = re.findall(r"Страна:\*\*.*?['|`](.*)['|`]", message.text)
    result_dict['vk-email'] = re.findall(r"Email:\*\*.*?['|`](.*)['|`]", message.text)
    result_dict['vk-twitter'] = re.findall(r"Twitter:\*\*.*?\[(.*)\]", message.text)
    result_dict['vk-instagram'] = re.findall(r"Instagram:\*\*.*?\[(.*)\]", message.text)
    result_dict['vk-home_phone'] = re.findall(r"Домашний:\*\* (.*)$", message.text)
    result_dict['vk-phone'] = re.findall(r"Мобильный:\*\* (.*)$", message.text)
    phones = re.findall(r"Телефоны:\*\* (.*)$", message.text)
    try:
        result_dict['phones-number'] = phones[0].split(',')
    except IndexError:
        result_dict['phones-number'] = phones
    return result_dict


async def Userbox(client, input_dict):
    channel_id = await client.get_entity('usersbox_bot')

    result_dict = dict()
    # Проходим по всем входным данным и прокидываем их через сервис
    for input_param in input_dict:
        async with client.conversation('@usersbox_bot') as conv:
            if input_param == 'IP_addresses-ip':
                # При запосе инфы об айпи - бот не догружает сообщение, поэтому просто ждем ответ
                await conv.send_message(input_dict[input_param])
                await conv.get_response()

                # Ждем последнее сообщение с информацией
                messages = await client.get_messages('@usersbox_bot', limit=1)

                result_dict = merge_two_dicts(result_dict, userbox_ip_parse(messages))
            else:
                # Ждем, когда бот догрузит всю инфу и изменит первое сообщение
                handle = conv.wait_event(events.MessageEdited(from_users=channel_id))

                # Прокидываем входные данные
                if input_param == 'instagram-id' or input_param == 'twitter-id' or input_param == 'facebook-id':
                    await conv.send_message('{}:"{}"'.format(input_param.split('-')[0], input_dict[input_param]))
                else:
                    await conv.send_message(input_dict[input_param])

                # Берем ответ и парсим его
                message_handle = await handle
                messages = message_handle.message

                # Парсим их и скидываем в результат
                if input_param == 'phones-number':
                    result_dict = merge_two_dicts(result_dict, userbox_phone_parse(messages))
                elif input_param == 'vk-id':
                    result_dict = merge_two_dicts(result_dict, userbox_vk_parse(messages))
                elif input_param == 'instagram-id':
                    result_dict = merge_two_dicts(result_dict, userbox_vk_parse(messages))
                elif input_param == 'twitter-id':
                    result_dict = merge_two_dicts(result_dict, userbox_vk_parse(messages))
                elif input_param == 'facebook-id':
                    result_dict = merge_two_dicts(result_dict, userbox_vk_parse(messages))

    return result_dict


async def GetContact(client, phone_number):
    async with client.conversation('@get_kontakt_bot') as conv:
        await conv.send_message(phone_number)

        response = await conv.get_response()
        message = response.text

        result_dict = dict()
        try:
            result_dict['phones-owner'] = re.search(r'Result \(.*?\): ok\n(.*)', message, re.S)[1].split('\n')
        except TypeError:
            pass

    return result_dict


async def FindNameVk(client, vk_id):
    async with client.conversation('@FindNameVk_bot') as conv:
        await conv.send_message(vk_id)

        response = await conv.get_response()
        message = response.text

        result_dict = dict()
        
        try:
            result_dict['vk-fio'] = re.search(r'удалось найти в интернете: (.*)', message)[1].split(', ')
        except TypeError:
            pass
        
        try:
            result_dict['vk-registered_date'] = re.search(r'Дата регистрации: (.*?)\n', message)[1],
        except TypeError:
            pass

    return result_dict


async def InfoVkUser(client, vk_id):
    channel_id = await client.get_entity('@infoVkUser_bot')
    async with client.conversation('@infoVkUser_bot') as conv:
        # Формируем ивент ответа сервиса
        message_patter = re.compile(r'.*?', re.M)
        handle = conv.wait_event(events.NewMessage(pattern=message_patter))

        # Прокидываем входные данные
        await conv.send_message(vk_id)

        # Берем ответ и парсим его
        message_handle = await handle
        message = message_handle.message

        result_dict = {}
        for button in message.buttons[0]:
            try:
                await button.click()
                message = await client.get_messages('@infoVkUser_bot', limit=1)

                message_after_click = message[0].text

                splitted_message = message_after_click.split('\n')
                # TODO: Если будет добавлена точность, то отделить количество людей и перевести в процент
                if "ВУЗам" in message_after_click:
                    result_dict['vk-fio'] = splitted_message[0]
                    result_dict['vk-University'] = splitted_message[4:7]
                if "городам" in message_after_click:
                    result_dict['vk-residential_address'] = splitted_message[4:7]
            except:
                pass

    return result_dict


async def AvinfoBotCar(client, car_number):
    async with client.conversation('@AvinfoBot') as conv:
        await conv.send_message(car_number)
        response = await conv.get_response()

        # Если нужно два сообщения последних забрать
        # async for message in client.iter_messages(channel_id, limit=2):
        #     print(message.sender_id, ':', message.text)
        # channel_id = await client.get_entity('AvinfoBot')

        information_dict = dict()
        response_text = str(response.text)
        # print(response_text)

        try:
            information_dict['car-subject'] = re.search(r'Субъект РФ: \*\*(.*?)\*\*', response_text)[1]
        except TypeError:
            pass

        try:
            information_dict['car-parking_session_number'] = \
            re.search(r'Парковочных сессий .*?: (\d{0,})', response_text)[1]
        except TypeError:
            pass

        dirty_info = re.findall(r'`(7[*0-9]{10})`((?:(?:, дата|, ФИО|, источник): \*\*.*?\*\*)?'
                                r'(?:(?:, дата|, ФИО|, источник): \*\*.*?\*\*)?'
                                r'(?:(?:, дата|, ФИО|, источник): \*\*.*?\*\*)?)', response_text)
        information_dict['car-owner'] = []
        for info in dirty_info:
            related_date = dict()
            related_date['phones-number'] = info[0]

            date = re.search(r', дата: \*\*(.*?)\*\*', info[1])
            nickname = re.search(r', ФИО: \*\*(.*?)\*\*', info[1])
            source = re.search(r', источник: \*\*(.*?)\*\*', info[1])

            if date is not None:
                related_date['car-date_appeal'] = date[1]
            if nickname is not None:
                related_date['nickname'] = nickname[1]
            if source is not None:
                related_date['car-other_information'] = source[1]

            information_dict['car-owner'].append(related_date)

        return information_dict


async def VKUserInfo(client, vk_id):
    async with client.conversation('@VKUserInfo_bot') as conv:
        await conv.send_message(vk_id)
        await conv.get_response()
        response = await conv.get_response()
        info = response.text
        information_dict = {}
        id = re.findall(r'ID:\s{1}(\d+)', info)[0]
        firsname = re.findall(r'Name:\s{1}(\w+)', info)[0]
        # lastname = re.findall(r'Last name:\s{1}(\w+)', info)[0]
        page_status = re.findall(r'Page privacy:\s{1}(\w+)', info)[0]
        last_seen = re.findall(r'Last seen:\s{1}([\w\s\-\:]+)\n', info)[0]
        platform = re.findall(r'Platform:\s{1}([\w]+)', info)[0]
        domain = re.findall(r'Domain:\s{1}([\w]+)', info)[0]
        # country = re.findall(r'Country:\s{1}([\w]+)', info)[0]
        city = re.findall(r'Location:\s{1}(.?)\n', info)[0]
        birthday = re.findall(r'Birthday:\s{1}([\w]+)', info)[0]
        registered = re.findall(r'Registered:\s{1}([\w\s\-\:]+)\n', info)[0]
        avatar = 'https://' + re.findall(r'Avatar:\s{1}([\w\/\.\-]+)', info)[0]
        resource = requests.get(avatar)
        photo = open(id + '.jpg', 'wb')
        photo.write(resource.content)
        photo.close()
        photo_path = os.path.abspath(id + '.jpg')

        information_dict['vk-name'] = firsname
        # information_dict['vk-surname'] = lastname
        information_dict['birthday'] = birthday
        information_dict['vk-page_status'] = page_status
        information_dict['vk-last_seen'] = last_seen
        information_dict['vk-platform'] = platform
        information_dict['vk-domain'] = domain
        # information_dict['vk-country'] = country
        information_dict['residential_address'] = city
        information_dict['vk-registered_date'] = registered
        information_dict['photo-path'] = photo_path
        return information_dict


async def Mailsearch(client, mail):
    async with client.conversation('@mailsearchbot') as conv:
        await conv.send_message(mail)
        response = await conv.get_response()
        info = response.text
        information_dict = {}
        passwords = re.findall(mail + r'\s*:\s*([\w\*]+)', info)
        information_dict['emails-user_name'] = mail
        information_dict['emails-password'] = passwords
        return information_dict


async def Shiver(client, mail):
    async with client.conversation('@shi_ver_bot') as conv:
        await conv.send_message('/q ' + mail)
        response = await conv.get_response()
        info = response.text
        information_dict = {}
        passwords = re.findall(mail + r'\s*:\s*([\w\*]+)', info)
        information_dict['emails-user_name'] = mail
        information_dict['emails-password'] = passwords
        return information_dict


async def WhoIsDom(client, domain):
    async with client.conversation('@WhoisDomBot') as conv:
        await conv.send_message(domain)
        response = await conv.get_response()
        info = response.text
        information_dict = {}
        ip = re.findall(r'\-*\s(\d{1,3}\.+\d{1,3}\.+\d{1,3}\.+\d{1,3})', info)
        if domain == []:
            domain = re.findall(r'domain:\*+\s{1}([\w\.]+)', info)
        registarID = re.findall(r'Registry Domain ID:\*+\s{1}([\w\-\_]+)', info)
        if registarID == []:
            registarID = re.findall(r'registrar:\*+\s{1}([\w\-]+)', info)
        creation_date = re.findall(r'Creation Date:\*+\s{1}([\w\-\:]+)', info)
        if creation_date == []:
            creation_date = re.findall(r'created:\*+\s{1}([\w\-\:]+)', info)
        nserver = re.findall(r'Name Server:\*+\s{1}([\w\.]+)', info)
        if nserver == []:
            nserver = re.findall(r'nserver:\*+\s{1}([\w\.]+)', info)
        information_dict['URL_addresses-ip'] = ip
        information_dict['URL_addresses-url'] = domain
        information_dict['URL_addresses-registar_id'] = registarID[0]
        information_dict['URL_addresses-creation_date'] = creation_date[0]
        information_dict['URL_addresses-nserver'] = nserver
        return information_dict

# client = ClientStart()
# with client:
#    output_data = client.loop.run_until_complete(VKUserInfo(client, id1))
