import os
import re
from time import time
import json
from pprint import pprint
from utils.smart_import import about_parameters_dict, get_service_functions, service_info_parser
from utils.neo4j_docker import SearchGraph, ResultSearchGraph
import itertools


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


def dict_search(dct, element):
    for key, value in dct.items():
        if element in value:
            return key
    return False


def combinations(data_dict, input_data, input_type):
    list_data = list(data_dict.values())
    list_data.append([input_data, ])

    result = []
    for length in range(1, len(list_data)+1):
        for c in itertools.combinations(list_data, length):
            for res in itertools.product(*c):
                result.append(res)

    result_combination = []
    for element_list in result:
        if len(element_list) == len(data_dict) + 1:
            combination = {}
            for element in element_list:
                if not dict_search(data_dict, element):
                    combination[input_type] = element
                else:
                    combination[dict_search(data_dict, element)] = element
            result_combination.append(combination)

    return result_combination


def create_service_input_data(service_info):
    with open('./utils/services_info.json', "r", encoding='windows-1251') as read_file:
        service_json = json.load(read_file)

    # Смотрим количество необходимых данных и берем их
    count_importance_data = 0
    service_input_data = []
    for json_input_data_type, json_input_data in service_json['service_info'][service_info['service_name']]['input_parameters'].items():
        # Такое условие потому, что этот json, если данные не обязательны имеет - onchange - без функции
        if len(json_input_data['onchange']) > 0:
            count_importance_data += 1
        if json_input_data_type != service_info['input_parameters']:
            service_input_data.append(json_input_data_type)

    return count_importance_data, service_input_data


def difficult_service_chain(result_graph, input_parameters, service_input_data, service_info, difficult_service_info):
    new_previous_data_service = {}
    if not isinstance(input_parameters, list):
        input_parameters = [input_parameters,]

    # Берем из предыдущего сервиса всех данные нужного типа и пробрасываем их в сервис
    for previous_data in input_parameters:
        # Забираем всевозможные данные уже имеющиеся в графе результата, которые необходимы сервису
        importance_data_result_graph = {}
        fullness_data_flag = True
        for input_data in service_input_data:
            importance_data_result_graph[input_data] = result_graph.search_data(input_data)
            if len(importance_data_result_graph[input_data]) == 0:
                fullness_data_flag = False

        # Если есть все нужные данные fullness_data_flag остался True
        if fullness_data_flag:
            # Вычисляем все возможные комбинации и прокидываем в сервис
            input_parameters_difficult_service = combinations(importance_data_result_graph,
                                                              previous_data,
                                                              service_info['input_parameters'])

            for input_parameter in input_parameters_difficult_service:
                # Проверяем прокидывали ли такое уже (через словарь сложных сервисов)
                # TODO: переписать проверку через граф поиска (все связи данных типво есть)
                if input_parameter not in difficult_service_info[service_info['service_name']]:
                    service_return = get_service_functions('search_type',
                                                           service_info['service_name'],
                                                           input_parameter)
                    result_graph.create_chain_result(service_return)
                    difficult_service_info[service_info['service_name']].append(input_parameter)

                    # Сохраняем результаты возвращенные сервисом
                    # TODO: проверить для сервисов прокидывающих в себя
                    new_previous_data_service = dicts_merge(new_previous_data_service,
                                                            service_return['output_data'])
                # Если такое уже прокидывалось - берем эти данные и сохраняем их
                else:
                    new_previous_data_service = dicts_merge(new_previous_data_service,
                                                            result_graph.take_service_output(input_parameter,
                                                                                             service_info['service_name']))
    return new_previous_data_service


def service_chain(result_graph, input_parameters, service_info):
    new_previous_data_service = {}
    if not isinstance(input_parameters, list):
        input_parameters = [input_parameters,]

    for previous_data in input_parameters:

        # Проверяем прокидывали ли такое уже (через граф результатов поиска)
        if not result_graph.check_graph_result(service_info['input_parameters'], previous_data, service_info['service_name']):
            service_return = get_service_functions('search_type', service_info['service_name'],
                                                   {service_info['input_parameters']: previous_data})
            result_graph.create_chain_result(service_return)

            # Сохраняем результаты возвращенные сервисом
            # TODO: проверить для сервисов прокидывающих в себя
            new_previous_data_service = dicts_merge(new_previous_data_service, service_return['output_data'])
        else:
            new_previous_data_service = dicts_merge(new_previous_data_service,
                                                    result_graph.take_service_output(
                                                        {service_info['input_parameters']: previous_data},
                                                        service_info['service_name']))

    return new_previous_data_service


def get_chains_function(chain_name, input_parameters):
    # start_time = time()
    start_time = '16173080990.245836'
    output_data = chains_list[chain_name]['output']
    difficult_service = {}
    # my_paths = [[{'service_name': 'Get Contact', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Find Name Vk', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Info Vk User', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Info Vk User', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'universities-name'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'VKPhoto', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'VKUserInfo', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'vk-id'}, {'service_name': 'Get Contact', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'vk-id'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Get Contact', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Find Name Vk', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Info Vk User', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Info Vk User', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'universities-name'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'VKPhoto', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'VKUserInfo', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Find Name Vk', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Info Vk User', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Info Vk User', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'universities-name'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'VKPhoto', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'VKUserInfo', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'vk-id'}, {'service_name': 'Get Contact', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'vk-id'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Get Contact', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Find Name Vk', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Info Vk User', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Info Vk User', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'universities-name'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'VKPhoto', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'VKUserInfo', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}], [{'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'phones-number'}, {'service_name': 'Userbox', 'input_parameters': 'vk-id'}, {'service_name': 'Fio Uni', 'input_parameters': 'fio'}]]

    for parameter, data in input_parameters.items():
        # Взяли все пути между входными и выходными данными
        # paths = my_paths
        search_graph = SearchGraph('searchgraph')
        paths = search_graph.path_between_nodes(parameter, output_data)
        result_graph = ResultSearchGraph(chain_name, 'chain', start_time)
        for path in paths:
            previous_data_service = input_parameters
            for service in path:
                if len(previous_data_service) != 0 and service['input_parameters'] in previous_data_service.keys():

                    # Смотрим количество необходимых данных и берем их
                    count_importance_data, service_input_data = create_service_input_data(service)

                    # Если обязательных входных данных больше 1 -
                    # добавляем в словарь "сложных сервисов" (сервисы имеющие больше 1 обязтаельного параметра на вход)
                    # Дальше прокидываем данные из прошлого сервиса со всеми имеющимися другими уже имеющимимся в графе
                    # результатов, при этом смотрим не было ли уже такой прокидки по словарю сложных сервисов
                    if count_importance_data > 1:

                        # Если такого не было - добавляем
                        if service['service_name'] not in difficult_service.keys():
                            difficult_service[service['service_name']] = []

                        # Берем из предыдущего сервиса всех данные нужного типа и пробрасываем их в сервис
                        new_previous_data_service = difficult_service_chain(result_graph,
                                                                            previous_data_service[service['input_parameters']],
                                                                            service_input_data, service,
                                                                            difficult_service)
                    else:
                        new_previous_data_service = service_chain(result_graph,
                                                                  previous_data_service[service['input_parameters']],
                                                                  service)
                    previous_data_service = new_previous_data_service
    print('VSE!!!!!')

# PhoneUniverDate16173080990245836
# get_chains_function('Phone Univer Date', {'phones-number': '89265512994'})
