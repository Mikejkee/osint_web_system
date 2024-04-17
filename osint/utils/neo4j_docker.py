from os import mkdir, listdir, path, unlink
import docker
from py2neo import Graph, Node, Relationship
from neo4j import GraphDatabase
import re
import paramiko
from pprint import pprint
import shutil
from time import time

# match (n)-[r]-() DELETE n,r;
# match (n) DELETE n;

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
        restart_neo4j()


class Neo4jGraph:
    """  Подключение к определенной бд, если она существует, либо ее создание - если нет  """

    def __init__(self, database_name):
        self.database_name = database_name
        scheme = "neo4j"
        host_name = "neo4j"
        port = 7687
        self.uri = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
        edit_config(self.database_name)
        self.graph = GraphDatabase.driver(self.uri, auth=('neo4j', 'neo4j'))

    def delete_bd(self):
        # Удаление определенной бд, при этом подключение будет к neo4j (не факт, что нужно)
        deleted_bd = self.database_name

        # Переподключаемся к стандартной бд
        self.database_name = 'neo4j'
        edit_config(self.database_name)
        self.graph = GraphDatabase.driver(self.uri)

        # Удаляем старую бд(стрираем из папок - данные и транзакции)
        shutil.rmtree('search_result/neo4j_data/databases/{}'.format(deleted_bd))
        shutil.rmtree('search_result/neo4j_data/transactions/{}'.format(deleted_bd))

    def close(self):
        self.graph.close()


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
        with self.graph.session() as session:
            session.run(create_data_node.format(data_type='car-number'))
            session.run(create_data_node.format(data_type='car-vin'))
            session.run(create_data_node.format(data_type='fio'))
            session.run(create_data_node.format(data_type='phones-number'))
            session.run(create_data_node.format(data_type='car-info'))
            session.run(create_data_node.format(data_type='telegram-id'))
            session.run(create_data_node.format(data_type='vk-id'))
            session.run(create_data_node.format(data_type='twitter-id'))
            session.run(create_data_node.format(data_type='instagram-id'))
            session.run(create_data_node.format(data_type='password'))
            session.run(create_data_node.format(data_type='emails-user_name'))
            session.run(create_data_node.format(data_type='residence_address'))
            session.run(create_data_node.format(data_type='universities-name'))
            session.run(create_data_node.format(data_type='date_of_birth'))
            session.run(create_data_node.format(data_type='photo-path'))
            session.run(create_data_node.format(data_type='universities-start_date'))
    
            session.run(create_service_node.format(service_name='Avinfo Bot Car'))
            session.run(create_service_node.format(service_name='Vin01'))
            session.run(create_service_node.format(service_name='Get Contact'))
            session.run(create_service_node.format(service_name='Userbox'))
            session.run(create_service_node.format(service_name='Find Name Vk'))
            session.run(create_service_node.format(service_name='Info Vk User'))
            session.run(create_service_node.format(service_name='VKPhoto'))
            session.run(create_service_node.format(service_name='VKUserInfo'))
            session.run(create_service_node.format(service_name='Shiver'))
            session.run(create_service_node.format(service_name='Fio Uni'))
    
            session.run(match_data_service_node_query.format(data_type='car-number', service_name='Avinfo Bot Car',
                                                                from_service='by_self'))
            session.run(
                match_data_service_node_query.format(data_type='car-number', service_name='Vin01', from_service='by_self'))
            session.run(
                match_data_service_node_query.format(data_type='car-vin', service_name='Vin01', from_service='by_self'))
            session.run(match_data_service_node_query.format(data_type='phones-number', service_name='Get Contact',
                                                                from_service='Avinfo Bot Car'))
            session.run(match_data_service_node_query.format(data_type='phones-number', service_name='Userbox',
                                                                from_service='Avinfo Bot Car'))
            session.run(match_data_service_node_query.format(data_type='vk-id', service_name='Find Name Vk',
                                                                from_service='Userbox'))
            session.run(match_data_service_node_query.format(data_type='vk-id', service_name='Info Vk User',
                                                                from_service='Userbox'))
            session.run(
                match_data_service_node_query.format(data_type='vk-id', service_name='VKPhoto', from_service='Userbox'))
            session.run(
                match_data_service_node_query.format(data_type='vk-id', service_name='VKUserInfo', from_service='Userbox'))
            session.run(
                match_data_service_node_query.format(data_type='vk-id', service_name='Userbox', from_service='Userbox'))
            session.run(match_data_service_node_query.format(data_type='phones-number', service_name='Userbox',
                                                                from_service='Userbox'))
            session.run(match_data_service_node_query.format(data_type='emails-user_name', service_name='Shiver',
                                                                from_service='Userbox'))
            session.run(
                match_data_service_node_query.format(data_type='fio', service_name='Fio Uni', from_service='Userbox'))
            session.run(match_data_service_node_query.format(data_type='universities-name', service_name='Fio Uni',
                                                                from_service='Userbox'))
    
            session.run(match_service_data_node_query.format(service_name='Avinfo Bot Car', data_type='fio'))
            session.run(match_service_data_node_query.format(service_name='Avinfo Bot Car', data_type='phones-number'))
            session.run(match_service_data_node_query.format(service_name='Vin01', data_type='car-info'))
            session.run(match_service_data_node_query.format(service_name='Get Contact', data_type='fio'))
            session.run(match_service_data_node_query.format(service_name='Userbox', data_type='fio'))
            session.run(match_service_data_node_query.format(service_name='Userbox', data_type='telegram-id'))
            session.run(match_service_data_node_query.format(service_name='Userbox', data_type='vk-id'))
            session.run(match_service_data_node_query.format(service_name='Userbox', data_type='phones-number'))
            session.run(match_service_data_node_query.format(service_name='Userbox', data_type='twitter-id'))
            session.run(match_service_data_node_query.format(service_name='Userbox', data_type='instagram-id'))
            session.run(match_service_data_node_query.format(service_name='Userbox', data_type='password'))
            session.run(match_service_data_node_query.format(service_name='Userbox', data_type='emails-user_name'))
            session.run(match_service_data_node_query.format(service_name='Find Name Vk', data_type='fio'))
            session.run(match_service_data_node_query.format(service_name='Find Name Vk', data_type='residence_address'))
            session.run(match_service_data_node_query.format(service_name='Info Vk User', data_type='fio'))
            session.run(match_service_data_node_query.format(service_name='Info Vk User', data_type='residence_address'))
            session.run(match_service_data_node_query.format(service_name='Info Vk User', data_type='universities-name'))
            session.run(match_service_data_node_query.format(service_name='VKPhoto', data_type='fio'))
            session.run(match_service_data_node_query.format(service_name='VKPhoto', data_type='residence_address'))
            session.run(match_service_data_node_query.format(service_name='VKPhoto', data_type='date_of_birth'))
            session.run(match_service_data_node_query.format(service_name='VKUserInfo', data_type='fio'))
            session.run(match_service_data_node_query.format(service_name='VKUserInfo', data_type='date_of_birth'))
            session.run(match_service_data_node_query.format(service_name='VKUserInfo', data_type='photo-path'))
            session.run(match_service_data_node_query.format(service_name='VKUserInfo', data_type='residence_address'))
            session.run(match_service_data_node_query.format(service_name='Shiver', data_type='password'))
            session.run(
                match_service_data_node_query.format(service_name='Fio Uni', data_type='universities-start_date'))

    def path_between_nodes(self, first_data_type, second_data_type):
        with self.graph.session() as session:
            result_transaction = session.write_transaction(self._return_path_between_nodes, first_data_type, second_data_type)
            return result_transaction

    @staticmethod
    def _return_path_between_nodes(tx, first_data_type, second_data_type):
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

        paths = tx.run(query.format(first_data=first_data_type, second_data=second_data_type))
        values = []
        for ix, record in enumerate(paths):
            values.append(record.value())
        list_all_path = []
        for path in values:
            list_path = []
            for node in path.nodes:
                if path.nodes.index(node) % 2 == 0:
                    parameters = node['data_type']
                else:
                    list_path.append(dict(service_name=node['service_name'], input_parameters=parameters))
            list_all_path.append(list_path)

        return list_all_path


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

    # def __init__(self, database_name):
    #     super().__init__(database_name)

    def __init__(self, service_name, search_type, start_time):
        if search_type == "chain":
            # Имя для цепочек - "НАЗВАНИЕ_ЦЕПОЧКИ-TIMESTAMP НАЧАЛА ПОИСКА-SEARCH"
            database_name = '{}{}'.format(service_name.replace(' ', ''), str(start_time).replace('.', ''))
        else:
            # Имя для сервисов - "TIMESTAMP НАЧАЛА ПОИСКА"
            database_name = '{}-result'.format(start_time)
        super().__init__(database_name)

    def create_chain_result(self, search_dict, first_node=False):
        # TODO: протестить на сервисах, которые внутрь себя прокидывают (Smart_Search!)
        with self.graph.session() as session:
            first_node = session.write_transaction(self._match_graph)
            if len(first_node) == 0:
                first_node = True
            else:
                first_node = False

            # Приводим к нужному виду
            service_name = search_dict['service_info']['service_name']
            end_timestamp = search_dict['service_info']['timestamp_stop_search']

            session.write_transaction(self._create_service_node, service_name)
            search_dict = create_node_result_service(search_dict)

            for data, parameters in search_dict['search_result'].items():
                session.write_transaction(self._create_data_node, parameters['data_type'], data)
                session.write_transaction(self._match_service_data_query, parameters['service_name'],
                                          parameters['data_type'], data, parameters['receipt_timestamp'])

            for data, parameters in search_dict.items():
                if data != 'search_result':
                    if first_node:
                        session.write_transaction(self._create_data_node, parameters['data_type'], data)
                    session.write_transaction(self._match_data_service_query, parameters['data_type'], data,
                                              service_name, parameters['receipt_timestamp'], end_timestamp)

    @staticmethod
    def _create_service_node(tx, service_name):
        create_service_node = """
            MERGE (p:Service{{service_name:"{service_name}"}})
        """

        return tx.run(create_service_node.format(service_name=service_name))

    @staticmethod
    def _create_data_node(tx, data_type, data):
        create_data_node = """ 
            CREATE (u1:Data {{data_type: "{data_type}", data: "{data}"}})
        """

        return tx.run(create_data_node.format(data_type=data_type, data=data))

    @staticmethod
    def _match_service_data_query(tx, service_name, data_type, data, timestamp):
        match_service_data_query = """
            MATCH (a:Service), (b:Data) WHERE  
            a.service_name = "{service_name}" AND b.data_type = "{data_type}" AND b.data = "{data}" 
            CREATE (a)-[r:from_service {{receipt_timestamp: "{timestamp}" }}]->(b)  
        """

        return tx.run(match_service_data_query.format(service_name=service_name, data_type=data_type, data=data,
                                                      timestamp=timestamp))

    @staticmethod
    def _match_data_service_query(tx, data_type, data, service_name, timestamp, end_timestamp):
        match_data_service_query = """
                MATCH (a:Data), (b:Service) WHERE  
                a.data_type = "{data_type}" AND a.data = "{data}" AND b.service_name = "{service_name}" 
                CREATE (a)-[r:to_service {{receipt_timestamp: "{timestamp}", end_timestamp: "{end_timestamp}" }}]->(b)  
            """

        return tx.run(match_data_service_query.format(data_type=data_type, data=data, service_name=service_name,
                                                      timestamp=timestamp, end_timestamp=end_timestamp))

    @staticmethod
    def _match_graph(tx):
        match_graph = """
            MATCH (n) RETURN n LIMIT 1
        """

        return tx.run(match_graph).values()

    def check_graph_result(self, data_type, data, service_name):
        with self.graph.session() as session:
            return session.write_transaction(self._check_graph_result, data_type, data, service_name.replace(' ', ''))

    @staticmethod
    def _check_graph_result(tx, data_type, data, service_name):
        match_query = """
            MATCH (a:Data{{data_type:'{data_type}', data:'{data}'}})
            -[:to_service]-
            (b:Service{{service_name:'{service_name}'}}) 
            RETURN b
        """
        result = tx.run(match_query.format(data_type=data_type, data=data, service_name=service_name)).values()
        if len(result) == 0:
            return False
        else:
            return True

    def search_data(self, data_type):
        with self.graph.session() as session:
            return session.write_transaction(self._search_data, data_type)

    @staticmethod
    def _search_data(tx, data_type):
        search_query = """
            MATCH (a:Data{{data_type:'{data_type}'}}) 
            RETURN a
        """

        result = tx.run(search_query.format(data_type=data_type)).values()
        search_list_nodes = []
        for node in result:
            search_list_nodes.append(node[0]['data'])
        return search_list_nodes

    def take_service_output(self, input_parameter, service_name):
        data_type = list(input_parameter.keys())[0]
        data = list(input_parameter.values())[0]
        with self.graph.session() as session:
            timestamp = session.write_transaction(self._take_end_timestamp, data, data_type, service_name.replace(' ', ''))
            return session.write_transaction(self._take_service_output, service_name, timestamp[0])

    @staticmethod
    def _take_end_timestamp(tx, data, data_type, service_name):
        take_end_timestamp = """
            MATCH (a:Data{{data:'{data}', data_type:'{data_type}'}})
            -[r:`to_service`]->
            (s:Service {{ service_name:'{service_name}' }})
            RETURN r.end_timestamp
        """
        return tx.run(take_end_timestamp.format(data=data, data_type=data_type, service_name=service_name)).value()


    @staticmethod
    def _take_service_output(tx, service_name, timestamp):
        take_query = """
            MATCH (s:Service {{ service_name:'{service_name}' }})
            -[r:`from_service`]-> (a:Data)
            WHERE r.receipt_timestamp='{timestamp}'
            RETURN a
        """

        result = tx.run(take_query.format(service_name=service_name, timestamp=timestamp)).values()
        result_dict = {}
        for node in result:
            data_type = node[0]['data_type']
            data = node[0]['data']
            if data_type not in result_dict.keys():
                result_dict[data_type] = list()
            result_dict[data_type].append(data)
        return result_dict
