from datetime import datetime as dt
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def format_datetime(date_time):
    date = date_time.strftime("%d %B %Y %H:%M")
    if str(date)[0] == '0':
        date = date[1:]
    # date = date.split()
    # month = {
    #     'Январь': 'января',
    #     'Февраль': 'февраля',
    #     'Март': 'марта',
    #     'Апрель': 'апреля',
    #     'Май': 'мая',
    #     'Июнь': 'июня',
    #     'Июль': 'июля',
    #     'Август': 'августа',
    #     'Сентябрь': 'сентября',
    #     'Октябрь': 'октября',
    #     'Ноябрь': 'ноября',
    #     'Декабрь': 'декабря',
    # }
    # date[1] = month[date[1]]
    return date