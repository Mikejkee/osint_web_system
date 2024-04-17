from os import mkdir, listdir, path, unlink
import docker
from py2neo import Graph
import re
import paramiko
from pprint import pprint
import shutil
from time import time, sleep


utils_dir = './utils/neo4j/conf/'
# utils_dir = 'neo4j/conf/'


class DockerGraph:
    """Поднмиает граф neo4j в докере"""

    def __init__(self, info):
        self.name = info['name']
        self.path = info['path']

        # Создание пути к файлам графа, если не сущетвуют
        try:
            mkdir(self.path)
        except:
            pass

        # Для работыв в Linux
        # self.cli = docker.APIClient(base_url='unix:///var/run/docker.sock')

        # Для работы на Windows
        self.cli = docker.APIClient(base_url='npipe:////./pipe/docker_engine')

        self.container_id = self.cli.create_container(
            image='neo4j',
            # volumes=['d:/Ucheba/fourthsem/Sorokin/pythonProjects/docker/neo4j/data/'],
            ports=[7474, 7687],
            name=self.name,
            host_config=self.cli.create_host_config(
                privileged=True,
                binds=[
                    self.path + 'data/:/data',
                ],
                port_bindings={
                    7474: 7474,
                    7687: 7687,
                }
            ),
            environment=["NEO4J_AUTH=neo4j/123123"],
        )

    def up(self):
        """ Метод поднятие докера """
        self.cli.start(container=self.container_id.get('Id'))

    def down(self):
        """ Метод остановка докера """
        self.cli.stop(container=self.container_id.get('Id'))


def delete_folder(folder):
    for the_file in listdir(folder):
        file_path = path.join(folder, the_file)
        try:
            if path.isfile(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def restart_neo4j():
    # Подключаемя по ssh к контейнеру neo4j
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("neo4j", username="root", password="root")

    # Перезапускаем сервис с neo4j в супервизоре
    stdin, stdout, stderr = ssh.exec_command("supervisorctl restart neo", get_pty=True)
    result = stdout.read().splitlines()

    return result


def edit_config(database_name):
    # Открываем файл конфига
    with open('{}neo4j.conf'.format(utils_dir), 'r') as f:
        old_data = f.read()

    # Если бд не та - меняем ее название на нужное
    if 'dbms.default_database={}\n'.format(database_name) not in old_data:
        new_data = re.sub('dbms.default_database=(.*?)\n', 'dbms.default_database={}\n'.format(database_name), old_data)

        with open('{}neo4j.conf'.format(utils_dir), 'w') as f:
            f.write(new_data)

        # Рестартим бд
        print(restart_neo4j())


class Neo4jGraph:
    """  Подключение к определенной бд, если она существует, либо ее создание - если нет  """

    def __init__(self, database_name):
        self.database_name = database_name
        edit_config(self.database_name)
        sleep(10)
        self.graph = Graph(scheme="neo4j", host="neo4j", port=7687, name=self.database_name)
        sleep(5)

    def delete_bd(self):
        # Удаление определенной бд, при этом подключение будет к neo4j (не факт, что нужно)
        deleted_bd = self.database_name

        # Переподключаемся к стандартной бд
        self.database_name = 'neo4j'
        edit_config(self.database_name)
        self.graph = Graph(scheme="bolt", host="neo4j", port=7687, name=self.database_name)

        # Удаляем старую бд(стрираем из папок - данные и транзакции)
        shutil.rmtree('search_result/neo4j_data/databases/{}'.format(deleted_bd))
        shutil.rmtree('search_result/neo4j_data/transactions/{}'.format(deleted_bd))

    def pri(self):
        print(self.graph.run('MATCH (c) RETURN c'))


class SearchGraph(Neo4jGraph):
    """ Класс графа поиска """

    def __init__(self, database_name):
        super().__init__(database_name)

    # def __init__(self, service_name, search_type, start_time):
    #     if search_type == "chain":
    #         # Имя для цепочек - "НАЗВАНИЕ_ЦЕПОЧКИ-TIMESTAMP НАЧАЛА ПОИСКА-SEARCH"
    #         database_name = '{}-{}-search'.format(service_name.replace(' ', '_'), start_time)
    #     else:
    #         # Имя для сервисов - "TIMESTAMP НАЧАЛА ПОИСКА"
    #         database_name = '{}-search'.format(start_time)
    #     super().__init__(database_name)
    #
    def create_chain_search_graph(self, search_dict, first_node=None):
        create_data_node = """ CREATE (u1:Data {{data_type: "{data_type}", data: "{data}"}})"""
        create_service_node = """ 
            CREATE (u1:Service {{service_name: "{service_name}", 
            timestamp_start_search: "{timestamp_start}", timestamp_end_search: "{timestamp_end}"}})"""
        match_first_node_query = """
            MATCH (a:Data), (b:Service) WHERE a.data_type = "{data_type}" AND a.data = "{data}" AND 
            b.service_name = "{service_name}" AND b.timestamp_start_search = "{timestamp_start}" AND 
            b.timestamp_end_search = "{timestamp_end}"
            CREATE (a)-[r:by_hands]->(b)  
        """
        match_query = """
            MATCH (a:Service), (b:Service) WHERE  
            a.service_name = "{a_service_name}" AND a.timestamp_start_search = "{a_timestamp_start}" 
            AND a.timestamp_end_search = "{a_timestamp_end}" AND 
            b.service_name = "{b_service_name}" AND b.timestamp_start_search = "{b_timestamp_start}" 
            AND b.timestamp_end_search = "{b_timestamp_end}"
            CREATE (a)-[r:Data {{data_type: "{data_type}", data: "{data}"}}]->(b)  
        """

        # Отстраиваем входные данные
        for data, data_parameters in search_dict.items():
            if first_node is None:
                self.graph.run(create_data_node.format(data_type=data_parameters['data_type'], data=data))
            for service_name, parameters in data_parameters['service_result'].items():
                self.graph.run(create_service_node.format(service_name=service_name,
                                                          timestamp_start=parameters['timestamp_start_search'],
                                                          timestamp_end=parameters['timestamp_end_search']))
                if first_node is None:
                    self.graph.run(match_first_node_query.format(data_type=data_parameters['data_type'], data=data,
                                                                 service_name=service_name,
                                                                 timestamp_start=parameters['timestamp_start_search'],
                                                                 timestamp_end=parameters['timestamp_end_search']))
                else:
                    self.graph.run(match_query.format(a_service_name=first_node['service_name'],
                                                      a_timestamp_start=first_node['timestamp_start_search'],
                                                      a_timestamp_end=first_node['timestamp_end_search'],
                                                      b_service_name=service_name,
                                                      b_timestamp_start=parameters['timestamp_start_search'],
                                                      b_timestamp_end=parameters['timestamp_end_search'],
                                                      data_type=data_parameters['data_type'], data=data, ))
                if len(parameters['searching_output']) != 0:
                    # Создаем рекурсивно все связи
                    self.create_search_graph(parameters['searching_output'], {
                        'service_name': service_name,
                        'timestamp_start_search': parameters['timestamp_start_search'],
                        'timestamp_end_search': parameters['timestamp_end_search']
                    })

    def create_chain(self):
        create_data_node = """ CREATE (u1:Data {{data_type: "{data_type}"}})"""
        create_service_node = """ 
                    CREATE (u1:Service {{service_name: "{service_name}"}})"""
        match_data_service_node_query = """
                    MATCH (a:Data), (b:Service) WHERE a.data_type = "{data_type}" AND 
                    b.service_name = "{service_name}"
                    CREATE (a)-[r:to_service]->(b)  
                """
        match_service_data_node_query = """
                    MATCH (a:Service), (b:Data) WHERE a.service_name = "{service_name}" AND
                    b.data_type = "{data_type}" 
                    CREATE (a)-[r:from_service]->(b)  
                """
        match_query = """
                    MATCH (a:Service), (b:Service) WHERE  
                    a.service_name = "{a_service_name}" AND 
                    b.service_name = "{b_service_name}" 
                    CREATE (a)-[r:Data {{data_type: "{data_type}"}}]->(b)  
                """
        self.graph.run(create_data_node.format(data_type='car-number'))
        self.graph.run(create_data_node.format(data_type='car-vin'))
        self.graph.run(create_data_node.format(data_type='fio'))
        self.graph.run(create_data_node.format(data_type='phones-number'))
        self.graph.run(create_data_node.format(data_type='car-info'))
        self.graph.run(create_data_node.format(data_type='telegram-id'))
        self.graph.run(create_data_node.format(data_type='vk-id'))
        self.graph.run(create_data_node.format(data_type='twitter-id'))
        self.graph.run(create_data_node.format(data_type='instagram-id'))
        self.graph.run(create_data_node.format(data_type='password'))
        self.graph.run(create_data_node.format(data_type='emails-user_name'))
        self.graph.run(create_data_node.format(data_type='residence_address'))
        self.graph.run(create_data_node.format(data_type='universities-name'))
        self.graph.run(create_data_node.format(data_type='date_of_birth'))
        self.graph.run(create_data_node.format(data_type='photo-path'))
        self.graph.run(create_data_node.format(data_type='universities-start_date'))

        self.graph.run(create_service_node.format(service_name='Avinfo Bot Car'))
        self.graph.run(create_service_node.format(service_name='Vin01'))
        self.graph.run(create_service_node.format(service_name='Get Contact'))
        self.graph.run(create_service_node.format(service_name='Userbox'))
        self.graph.run(create_service_node.format(service_name='Find Name Vk'))
        self.graph.run(create_service_node.format(service_name='Info Vk User'))
        self.graph.run(create_service_node.format(service_name='VKPhoto'))
        self.graph.run(create_service_node.format(service_name='VKUserInfo'))
        self.graph.run(create_service_node.format(service_name='Shiver'))
        self.graph.run(create_service_node.format(service_name='Fio Uni'))

        self.graph.run(match_data_service_node_query.format(data_type='car-number', service_name='Avinfo Bot Car',
                                                            from_service='by_self'))
        self.graph.run(
            match_data_service_node_query.format(data_type='car-number', service_name='Vin01', from_service='by_self'))
        self.graph.run(
            match_data_service_node_query.format(data_type='car-vin', service_name='Vin01', from_service='by_self'))
        self.graph.run(match_data_service_node_query.format(data_type='phones-number', service_name='Get Contact',
                                                            from_service='Avinfo Bot Car'))
        self.graph.run(match_data_service_node_query.format(data_type='phones-number', service_name='Userbox',
                                                            from_service='Avinfo Bot Car'))
        self.graph.run(match_data_service_node_query.format(data_type='vk-id', service_name='Find Name Vk',
                                                            from_service='Userbox'))
        self.graph.run(match_data_service_node_query.format(data_type='vk-id', service_name='Info Vk User',
                                                            from_service='Userbox'))
        self.graph.run(
            match_data_service_node_query.format(data_type='vk-id', service_name='VKPhoto', from_service='Userbox'))
        self.graph.run(
            match_data_service_node_query.format(data_type='vk-id', service_name='VKUserInfo', from_service='Userbox'))
        self.graph.run(
            match_data_service_node_query.format(data_type='vk-id', service_name='Userbox', from_service='Userbox'))
        self.graph.run(match_data_service_node_query.format(data_type='phones-number', service_name='Userbox',
                                                            from_service='Userbox'))
        self.graph.run(match_data_service_node_query.format(data_type='emails-user_name', service_name='Shiver',
                                                            from_service='Userbox'))
        self.graph.run(
            match_data_service_node_query.format(data_type='fio', service_name='Fio Uni', from_service='Userbox'))
        self.graph.run(match_data_service_node_query.format(data_type='universities-name', service_name='Fio Uni',
                                                            from_service='Userbox'))

        self.graph.run(match_service_data_node_query.format(service_name='Avinfo Bot Car', data_type='fio'))
        self.graph.run(match_service_data_node_query.format(service_name='Avinfo Bot Car', data_type='phones-number'))
        self.graph.run(match_service_data_node_query.format(service_name='Vin01', data_type='car-info'))
        self.graph.run(match_service_data_node_query.format(service_name='Get Contact', data_type='fio'))
        self.graph.run(match_service_data_node_query.format(service_name='Userbox', data_type='fio'))
        self.graph.run(match_service_data_node_query.format(service_name='Userbox', data_type='telegram-id'))
        self.graph.run(match_service_data_node_query.format(service_name='Userbox', data_type='vk-id'))
        self.graph.run(match_service_data_node_query.format(service_name='Userbox', data_type='phones-number'))
        self.graph.run(match_service_data_node_query.format(service_name='Userbox', data_type='twitter-id'))
        self.graph.run(match_service_data_node_query.format(service_name='Userbox', data_type='instagram-id'))
        self.graph.run(match_service_data_node_query.format(service_name='Userbox', data_type='password'))
        self.graph.run(match_service_data_node_query.format(service_name='Userbox', data_type='emails-user_name'))
        self.graph.run(match_service_data_node_query.format(service_name='Find Name Vk', data_type='fio'))
        self.graph.run(match_service_data_node_query.format(service_name='Find Name Vk', data_type='residence_address'))
        self.graph.run(match_service_data_node_query.format(service_name='Info Vk User', data_type='fio'))
        self.graph.run(match_service_data_node_query.format(service_name='Info Vk User', data_type='residence_address'))
        self.graph.run(match_service_data_node_query.format(service_name='Info Vk User', data_type='universities-name'))
        self.graph.run(match_service_data_node_query.format(service_name='VKPhoto', data_type='fio'))
        self.graph.run(match_service_data_node_query.format(service_name='VKPhoto', data_type='residence_address'))
        self.graph.run(match_service_data_node_query.format(service_name='VKPhoto', data_type='date_of_birth'))
        self.graph.run(match_service_data_node_query.format(service_name='VKUserInfo', data_type='fio'))
        self.graph.run(match_service_data_node_query.format(service_name='VKUserInfo', data_type='date_of_birth'))
        self.graph.run(match_service_data_node_query.format(service_name='VKUserInfo', data_type='photo-path'))
        self.graph.run(match_service_data_node_query.format(service_name='Shiver', data_type='password'))
        self.graph.run(
            match_service_data_node_query.format(service_name='Fio Uni', data_type='universities-start_date'))

    def path_between_nodes(self, first_data_type, second_data_type):
        query = """
        MATCH (a:Data), (b:Data), paths = (a)-[*]->(b)
        WHERE a.data_type ='{first_data}' AND b.data_type = '{second_data}'
        Return paths
        """

        query_all_path = """
                MATCH (a:Data), (b:Data), paths = (a)-[*]->(b)
                WHERE  LENGTH(paths)>2
                Return paths
                """

        paths = self.graph.run(query.format(first_data=first_data_type, second_data=second_data_type)).data()
        list_all_path = []
        for path in paths:
            list_path = []
            for node in path['paths'].nodes:
                if path['paths'].nodes.index(node) % 2 == 0:
                    parameters = node['data_type']
                else:
                    list_path.append(dict(service_name=node['service_name'], input_parameters=parameters))
            list_all_path.append(list_path)

        return list_all_path


# g = SearchGraph('neo4j')
# g.create_chain()
# pprint(g.path_betwen_nodes('phones-number', 'universities-start_date'))

def create_result_graph_dict(data_type, service_name, timestamp):
    return {
        'data_type': data_type,
        'service_name': service_name,
        'receipt_timestamp': timestamp,
    }


def create_search_graph_dict(timestamp_start):
    return {
        'searching_output': {},
        'timestamp_start_search': timestamp_start,
        'timestamp_end_search': time()
    }


def parse_result_service(result_dict, service_name, timestamp):
    parse_dict = {}
    for result in result_dict:
        # Из HOW TO DO SERVICE.txt 2 пункт формирования output_data
        if isinstance(result_dict[result], list):
            for value in result_dict[result]:
                parse_dict[value] = create_result_graph_dict(result, service_name, timestamp)
        # Из HOW TO DO SERVICE.txt 3 пункт формирования output_data
        elif isinstance(result_dict[result], dict):
            for sub_result in result_dict[result]:
                parse_dict[sub_result] = create_result_graph_dict(result, service_name, timestamp)
                # Теперь проверяем для него значения
                for value in result_dict[result][sub_result]:
                    # Из HOW TO DO SERVICE.txt 2 пункт формирования output_data
                    if isinstance(result_dict[result][sub_result][value], list):
                        for list_value in result_dict[result][sub_result][value]:
                            parse_dict[sub_result]['search_result'][list_value] = create_result_graph_dict(
                                value, service_name, timestamp)
                    else:
                        # Из HOW TO DO SERVICE.txt 1 пункт формирования output_data
                        parse_dict[sub_result]['search_result'][
                            result_dict[result][sub_result][value]] = create_result_graph_dict(
                            value, service_name, timestamp)
        else:
            # Из HOW TO DO SERVICE.txt 1 пункт формирования output_data
            parse_dict[result_dict[result]] = create_result_graph_dict(result, service_name, timestamp)
    return parse_dict


def create_node_result_service(service_result):
    first_node = dict()
    for parameter in service_result['input_parameters']:
        first_node[parameter['data']] = dict(data_type=parameter['info_type'],
                                             service_name='by_self',
                                             receipt_timestamp=service_result['service_info']['timestamp_start_search'])
    first_node['search_result'] = dict()
    first_node['search_result'] = parse_result_service(service_result['output_data'],
                                                       service_result['service_info']['service_name'], service_result['service_info']['timestamp_stop_search'])
    return first_node


class ResultSearchGraph(Neo4jGraph):
    """ Класс графа резултата поиска """

    def __init__(self, service_name, search_type, start_time):
        if search_type == "chain":
            # Имя для цепочек - "НАЗВАНИЕ_ЦЕПОЧКИ-TIMESTAMP НАЧАЛА ПОИСКА-SEARCH"
            database_name = '{}{}'.format(service_name.replace(' ', ''), str(start_time).replace('.', ''))
        else:
            # Имя для сервисов - "TIMESTAMP НАЧАЛА ПОИСКА"
            database_name = '{}-result'.format(start_time)
        super().__init__(database_name)

    def create_result_search_graph(self, search_dict, first_node=None):
        create_data_node = """ 
            CREATE (u1:Data {{data_type: "{data_type}", data: "{data}", receipt_timestamp: "{timestamp}" }})
        """
        match_query = """
                MATCH (a:Data), (b:Data) WHERE  
                a.data_type = "{a_data_type}" AND a.data = "{a_data}" AND a.receipt_timestamp = "{a_timestamp}" AND 
                b.data_type = "{b_data_type}" AND b.data = "{b_data}" AND b.receipt_timestamp = "{b_timestamp}"
                CREATE (a)-[r:Service {{service_name: "{service_name}" }}]->(b)  
            """

        # Отстраиваем входные данные
        for data, data_parameters in search_dict.items():
            self.graph.run(create_data_node.format(data_type=data_parameters['data_type'], data=data,
                                                   timestamp=data_parameters['receipt_timestamp']))
            if first_node is not None:
                self.graph.run(match_query.format(a_data_type=first_node['data_type'],
                                                  a_data=first_node['data'],
                                                  a_timestamp=first_node['receipt_timestamp'],
                                                  b_data_type=data_parameters['data_type'],
                                                  b_data=data,
                                                  b_timestamp=data_parameters['receipt_timestamp'],
                                                  service_name=data_parameters['service_name']))
            for search_data, parameters in data_parameters['search_result'].items():
                self.graph.run(create_data_node.format(data_type=parameters['data_type'], data=search_data,
                                                       timestamp=parameters['receipt_timestamp']))
                self.graph.run(match_query.format(a_data_type=data_parameters['data_type'],
                                                  a_data=data,
                                                  a_timestamp=data_parameters['receipt_timestamp'],
                                                  b_data_type=parameters['data_type'],
                                                  b_data=search_data,
                                                  b_timestamp=parameters['receipt_timestamp'],
                                                  service_name=parameters['service_name']))
                if len(parameters['search_result']) != 0:
                    # Создаем рекурсивно все связи
                    self.create_result_search_graph(parameters['search_result'], {
                        'data': search_data,
                        'data_type': parameters['data_type'],
                        'receipt_timestamp': parameters['receipt_timestamp'],
                    })

    def create_chain_result(self, search_dict, first_node=False):
        # TODO: протестить на сервисах, которые внутрь себя прокидывают (Smart_Search!)
        create_data_node = """ 
            CREATE (u1:Data {{data_type: "{data_type}", data: "{data}"}})
        """
        create_service_node = """
            MERGE (p:Service{{service_name:"{service_name}"}})
        """
        match_service_data_query = """
                MATCH (a:Service), (b:Data) WHERE  
                a.service_name = "{service_name}" AND b.data_type = "{data_type}" AND b.data = "{data}" 
                CREATE (a)-[r:from_service {{receipt_timestamp: "{timestamp}" }}]->(b)  
            """
        match_data_service_query = """
                MATCH (a:Data), (b:Service) WHERE  
                a.data_type = "{data_type}" AND a.data = "{data}" AND b.service_name = "{service_name}" 
                CREATE (a)-[r:to_service {{receipt_timestamp: "{timestamp}", end_timestamp: "{end_timestamp}" }}]->(b)  
            """
        match_graph = """
            MATCH (n) RETURN n LIMIT 1
        """
        first_node = self.graph.run(match_graph).data()
        if len(first_node) == 0:
            first_node = True
        else:
            first_node = False
        # Приводим к нужному виду
        service_name = search_dict['service_info']['service_name']
        end_timestamp = search_dict['service_info']['timestamp_stop_search']
        self.graph.run(create_service_node.format(service_name=service_name))
        search_dict = create_node_result_service(search_dict)

        for data, parameters in search_dict['search_result'].items():
            self.graph.run(create_data_node.format(data_type=parameters['data_type'], data=data))
            self.graph.run(match_service_data_query.format(service_name=parameters['service_name'],
                                                           data_type=parameters['data_type'], data=data,
                                                           timestamp=parameters['receipt_timestamp']))


        for data, parameters in search_dict.items():
            if data != 'search_result':
                if first_node:
                    self.graph.run(create_data_node.format(data_type=parameters['data_type'], data=data,
                                                           timestamp=parameters['receipt_timestamp']))
                self.graph.run(match_data_service_query.format(data_type=parameters['data_type'], data=data,
                                                               service_name=service_name,
                                                               timestamp=parameters['receipt_timestamp'],
                                                               end_timestamp=end_timestamp))

    def check_graph_result(self, data_type, data, service_name):
        match_query = """
            MATCH (a:Data{{data_type:'{data_type}', data:'{data}'}})
            -[:to_service]-
            (b:Service{{service_name:'{service_name}'}}) 
            RETURN b
        """
        result = self.graph.run(match_query.format(data_type=data_type, data=data, service_name=service_name.replace(' ', '')))
        if len(result.data()) == 0:
            return False
        else:
            return True

    def search_data(self, data_type):
        search_query = """
            MATCH (a:Data{{data_type:'{data_type}'}}) 
            RETURN a
        """
        result = self.graph.run(search_query.format(data_type=data_type)).data()
        search_list_nodes = []
        for node in result:
            search_list_nodes.append(node['a']['data'])
        return search_list_nodes

    def take_service_output(self, input_parameter, service_name):
        take_end_timestamp = """
            MATCH (a:Data{{data:'{data}', data_type:'{data_type}'}})
            -[r:`to_service`]->
            (s:Service {{ service_name:'{service_name}' }})
            RETURN r.end_timestamp
        """
        take_query = """
            MATCH (s:Service {{ service_name:'{service_name}' }})
            -[r:`from_service`]-> (a:Data)
            WHERE r.receipt_timestamp='{timestamp}'
            RETURN a
        """

        data_type = list(input_parameter.keys())[0]
        data = list(input_parameter.values())[0]
        timestamp = self.graph.run(take_end_timestamp.format(data=data, data_type=data_type, service_name=service_name.replace(' ', ''))).data()[0]['r.end_timestamp']
        output_data = self.graph.run(take_query.format(service_name=service_name, timestamp=timestamp))
        result_dict = {}
        for node in output_data.data():
            data_type = node['a']['data_type']
            data = node['a']['data']
            if data_type not in result_dict.keys():
                result_dict[data_type] = list()
            result_dict[data_type].append(data)

        return result_dict

# g = SearchGraph('neo4j')
# g.create_chain()
# g = ResultSearchGraph('neo4j')
# g.take_service_output(inpt, 'Userbox')
# print(g.search_data_graph_result('vk-email'))
# g.create_chain_result(service_result)
# print(g.search_data('vk-email'))