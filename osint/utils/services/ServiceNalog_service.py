from utils.services.my_service.OSINT import ServiceNalog
from time import time

"""
    "service_name": "Service Nalog",
    "input_parameters": "[!surname, !name, !patronymic, !date_of_birth, !passports-serial, !passports-number, !passports-issue_date]",
    "Description": "Service Nalog Parser info INPUT(surname, name), OUTPUT(ИНН)", 
"""

def main(input_parameters):
    start_time = time()
    surname = input_parameters['surname']
    name = input_parameters['name']
    patronymic = input_parameters['patronymic']
    date_of_birth = input_parameters['date_of_birth']
    passports_serial = input_parameters['passports-serial']
    passports_number = input_parameters['passports-number']
    passports_issue_date = input_parameters['passports-issue_date']
    profile = ServiceNalog(surname, name, patronymic, date_of_birth, passports_serial, passports_number, passports_issue_date)
    profile.search()
    output_data = profile.get_info()
    return_dic = {
        'input_parameters':
        [
            {
                "info_type": "vk-surname",
                "data": surname
            },
            {
                "info_type": "vk-name",
                "data": name
            },
            {
                "info_type": "patronymic",
                "data": patronymic
            },
            {
                "info_type": "date_of_birth",
                "data": date_of_birth
            },
            {
                "info_type": "passports-serial",
                "data": passports_serial
            },
            {
                "info_type": "passports-number",
                "data": passports_number
            },
            {
                "info_type": "passports-issue_date",
                "data": passports_issue_date
            },
        ],
        'service_info': {
            "service_name": "Service Nalog",
            'timestamp_start_search': start_time,
            'timestamp_stop_search': time(),
        },
        'output_data': output_data,
    }
    return return_dic
