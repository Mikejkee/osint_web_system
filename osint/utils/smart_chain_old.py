import os
import re
import json
from pprint import pprint
from smart_import import about_parameters_dict, get_service_functions, service_info_parser
from neo4j_docker import SearchGraph, ResultSearchGraph


chains_list = {
    'Car Fio': dict(input_parameters=['!car-number', ], output='fio',
                   description='Ищем по номеру машины возможное ФИО владельца'),
    'Phone Univer Date': dict(input_parameters=['!phones-number', ], output='universities-start_date',
                    description='Ищем по номеру телефона возможный год поступления'),
    'Phone Photo': dict(input_parameters=['!phones-number', ], output='photo',
                        description='Ищем по тф номеру фотографию владельца'),
    'Phone Address': dict(input_parameters=['!phones-number', ], output='residence_address',
                          description='Ищем по тф номеру адрес'),
    'Instagram Birth': dict(input_parameters=['!instagram-id', ], output='date_of_birth',
                            description='Ищем по инстаграмму дату рождения'),
}


def chain_info_parser():
    chain_list_info = []
    # Проходим по всем цепочкам, парсим их описание
    for chain, info in chains_list.items():

        # Вытаскиваем описание
        chain_name = chain
        input_parameters = info['input_parameters']

        # Формируем обязательные и не обязательные параметры
        edited_input_parameters = []
        for input_parameter in input_parameters:
            if input_parameter[0] == '!':
                edited_input_parameters.append({'importance': 1, 'value': input_parameter[1:]})
            else:
                edited_input_parameters.append({'importance': 0, 'value': input_parameter})

        description = info['description']
        chain_list_info.append({
            'chain_name': chain_name,
            'input_parameters': edited_input_parameters,
            'description': description,
        })

    return chain_list_info


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
        json.dump(output_info, file, sort_keys=False, ensure_ascii=False, )
    pprint(output_info)


def dicts_merge(first_dict, second_dict):
    # Проходим по словарю и рассматрвиаем различные варианты составных элементов для мерджа
    for second_dict_elem in second_dict:
        # Если такой элемент словаря уже есть в первом
        if second_dict_elem in first_dict:
            # Если он список и добавляемый элемент из друго словаря - список, просто складывавем списки, если они не равны
            if isinstance(first_dict[second_dict_elem], list) and isinstance(second_dict[second_dict_elem], list):
                first_dict[second_dict_elem] = list(set(first_dict[second_dict_elem] + second_dict[second_dict_elem]))
            # Если он список и добавляемый элемент из друго словаря - не список, делаем из второго список и складываем
            elif isinstance(first_dict[second_dict_elem], list) and type(second_dict[second_dict_elem]) is not list:
                first_dict[second_dict_elem] = list(set(first_dict[second_dict_elem] + [second_dict[second_dict_elem]]))
            # Если он не список и добавляемый элемент из друго словаря - список, делаем из первого список и складываем
            elif type(first_dict[second_dict_elem]) is not list and isinstance(second_dict[second_dict_elem], list):
                first_dict[second_dict_elem] = list(set([first_dict[second_dict_elem]] + second_dict[second_dict_elem]))
            # Если он не список и добавляемый элемент из друго словаря - не список,
            # делаем из первого и второго список и складываем
            elif type(first_dict[second_dict_elem]) is not list and type(second_dict[second_dict_elem]) is not list:
                first_dict[second_dict_elem] = list(set([first_dict[second_dict_elem]] + [second_dict[second_dict_elem]]))
        # Если элемента вообще не было - создаем
        else:
            first_dict[second_dict_elem] = second_dict[second_dict_elem]

    return first_dict


def result_graph_value_exist_check(graph):
    return 1


def get_chains_function(chain_name, input_parameters):
    output_data = chains_list[chain_name]['output']
    search_graph = SearchGraph('neo4j')
    result_graph = ResultSearchGraph('neo4j')
    difficult_service = {}
    with open('services_info.json', "r", encoding='windows-1251') as read_file:
        service_json = json.load(read_file)

    for parameter, data in input_parameters.items():
        # Взяли все пути между входными и выходными данными
        paths = search_graph.path_between_nodes(parameter, output_data)
        for path in paths:
            previos_data_service = input_parameters
            for service in path:
                # 1 Написать для самого первогр поиска постройку графа результатов
                # if paths.index(path) == 0:
                #     result_graph.create_chain_result(service_return, True)
                # Мы сначала смотрим на необходимые входные данные для этого сервиса, если необходимых данных
                # по количеству > 2,
                # то мы запрашиваем в графе резульатов все данные этих типов
                # 3. и для каждой пары (тройки т тд, смотря сколько их в количестве) прокидывваем в сервис,
                # 4. если они уже не были прокинуты, т.е. в графе результатов не сущетсвует такой ветки.
                # 5. Если необходим 1 тип данных, то мы их смотрим только из результатов предыдущего сервиса

                # Смотрим количество необходимых данных и берем их
                # count_importance_data = 0
                # service_input_data = []
                # for json_input_data in service_json['service_info'][service['service_name']]['input_parameters']:
                #     # Такое условие потому, что этот json, если данные не обязательны имеет - onchange - без функции
                #     if len(json_input_data['onchange']) > 0:
                #         count_importance_data += 1
                #     service_input_data.append(json_input_data)

                # Если обязательных входных данных больше 2 -
                # добавляем в словарь "сложных сервисов" (сервисы имеющие больше 2 обязтаельных параметров на вход)
                # Дальше прокидываем данные из прошлого сервиса со всеми имеющимися другими, при этом смотрим не было ли
                # уже такой прокидки по словарю
                # if count_importance_data > 1:
                #     # Если такого не было - добавляем
                #     if service['service_name'] not in difficult_service.keys():
                #         for input_data in service_input_data:
                #                 difficult_service[service['service_name']][input_data] = []
                #     else:
                #         for input_data in service_input_data:
                #             if input_data in previos_data_service:

                # Берем из предыдущего сервиса всех данные нужного типа и пробрасываем их в сервис
                new_previos_data_service = {}
                if isinstance(previos_data_service[service['input_parameters']], list):
                    for previos_data in previos_data_service[service['input_parameters']]:
                        # Проверяем прокидывали ли такое уже (через граф результатов поиска)
                        exist_flag = False
                        if not result_graph.check_graph_result(service['input_parameters'], previos_data, service['service_name']):
                            exist_flag = True
                        # Если такой сервис не был с такими входными данными, то прокидываем и отстраиваем граф результатов
                        if exist_flag:
                            service_return = get_service_functions('search_type', service['service_name'],
                                                                   {service['input_parameters']: previos_data})
                            result_graph.create_chain_result(service_return)

                        # Сохраняем результаты возвращенные сервисом
                        # TODO: проверить для сервисов прокидывающих в себя
                        new_previos_data_service = dicts_merge(new_previos_data_service, service_return['output_data'])
                else:
                    # Проверяем прокидывали ли такое уже (через граф результатов поиска)
                    exist_flag = False
                    if not result_graph.check_graph_result(service['input_parameters'], previos_data_service[service['input_parameters']],
                                                           service['service_name']):
                        exist_flag = True
                    # Если такой сервис не был с такими входными данными, то прокидываем и отстраиваем граф результатов
                    if exist_flag:
                        service_return = get_service_functions('search_type', service['service_name'],
                                                               {service['input_parameters']: previos_data_service[service['input_parameters']]})
                        result_graph.create_chain_result(service_return)

                    # Сохраняем результаты возвращенные сервисом
                    # TODO: проверить для сервисов прокидывающих в себя
                    new_previos_data_service = dicts_merge(new_previos_data_service, service_return['output_data'])

                previos_data_service = new_previos_data_service

get_chains_function('Phone Univer Date', {'phones-number': '89265512994'})

# create_chain_info()


# data_dict_graph_result = dict()
# if count_importance_data > 1:
#     for input_data in service_input_data:
#         data_dict_graph_result[input_data] = result_graph.search_data_graph_result(input_data)
#
#     # 3. и для каждой пары (тройки т тд, смотря сколько их в количестве) прокидывваем в сервис,
#     # 4. если они уже не были прокинуты, т.е. в графе результатов не сущетсвует такой ветки.
#     exist_flag = False
#     exist_values_dict = dict()
#     not_exist_values_dict = {}
#     for input_parameter in data_dict_graph_result:
#         for input_parameter_data in input_parameter:
#             if result_graph.check_graph_result(input_parameter, service['input_parameters'][input_parameter],
#                                                service['service_name']):
#
