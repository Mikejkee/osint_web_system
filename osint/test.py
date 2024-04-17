from py2neo import Graph, Node, Relationship

graph = Graph(scheme="bolt", host="127.0.0.1", port=7687)


info = {'input_parameters': [{'info_type': 'name', 'data': 'Диман'}, {'info_type': 'surname', 'data': 'Курпатов'},
                             {'info_type': 'phones-number', 'data': '878998'}],
        'service_info': {'service_name': 'Test Service Telephone Info', 'search_timestamp': 1587834223.7442484},
        'output_data': [{'patronymic': 'Test1',
                         'phones': [{'phones-phone_type': 'Свой1', 'phones-model': 'Iphone', 'phones-comment': 'Постоянно юзает его'}]
                         },
                        {'patronymic': 'Test2',
                         'phones': [
                             {'phones-phone_type': 'Свой1', 'phones-model': 'Samsung', 'phones-comment': 'Разовый'},
                             {'phones-phone_type': 'Свой2', 'phones-model': 'Samsung', 'phones-comment': 'Постоянный'},
                             {'phones-phone_type': 'Свой3', 'phones-model': 'Samsung', 'phones-comment': 'Отца'},
                         ],
                        'vk': [
                             {'vk-phone_type': 'Свой1', 'vk-model': 'Samsung', 'vk-comment': 'Разовый'},
                             {'vk-phone_type': 'Свой2', 'vk-model': 'Samsung', 'vk-comment': 'Постоянный'},
                             {'vk-phone_type': 'Свой3', 'vk-model': 'Samsung', 'vk-comment': 'Отца'},
                         ]
                         },
                        {'patronymic': 'Test3',
                         'phones': [{'phones-phone_type': 'Брата', 'phones-model': 'Huawei', 'phones-comment': 'Домашний'}]
                         }]
        }

search_count = 0
for data_part in info['output_data']:
    # Создали вершину номера поискового результата
    search_result_node = Node('search_result', name='search_result_'+str(search_count))

    # Соединили с входными параметрами
    for parameter in info['input_parameters']:
        parent_node = Node(parameter['info_type'], name=parameter['data'])
        SERVICE = Relationship.type(info['service_info']['service_name'])
        graph.merge(SERVICE(parent_node, search_result_node), 'timestamp', "name")

    # Создаем непосредсвенно резултат поиска
    for data_type in data_part:
        data_type_value = data_part[data_type]

        # Если уже результат (то есть значение типа данных является строкой), то просто соединяем с номером поискового результата
        if type(data_type_value) is str:
            children_result_node = Node(data_type, name=data_type_value)
            RESULT = Relationship.type('Result Information')
            graph.merge(RESULT(search_result_node, children_result_node), 'timestamp', "name")

        # Иначе это список объектов со свойствами
        else:
            type_result_count = 0
            for data_objects in data_type_value:
                children_object_node = Node(data_type, name='{}_{}'.format(data_type, str(type_result_count)))
                OBJECT = Relationship.type('Result object')
                graph.merge(OBJECT(search_result_node, children_object_node), 'timestamp', "name")
                type_result_count +=1
                # for parameter in info['input_parameters']:
                #     parent_node = Node(parameter['info_type'], name=parameter['data'])
                #     SERVICE = Relationship.type(info['service_info']['service_name'])
                #     graph.merge(SERVICE(parent_node, parent_list_node), 'timestamp', "name")
                # for data_type_dict in data_value:
                #     for parameter in data_type_dict:
                #         parameter_value = data_type_dict[parameter]
                #         children_list_node = Node(parameter, name=parameter_value)
                #         INFO = Relationship.type('info')
                #         graph.merge(INFO(parent_list_node, children_list_node), 'timestamp', "name")
                # _id += 1

    search_count += 1



    #
    #     else:
    #
    # search_count += 1
