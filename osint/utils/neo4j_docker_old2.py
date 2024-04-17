from os import mkdir, listdir, path, unlink
import docker
from py2neo import Graph, Node, Relationship
import re
import paramiko
import shutil

# match (n)-[r]-() DELETE n,r;
# match n DELETE n;

utils_dir = './utils/neo4j/conf/'
#utils_dir = 'neo4j/conf/'


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
            elif path.isdir(file_path): shutil.rmtree(file_path)
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
        edit_config(self.database_name)
        self.graph = Graph(scheme="bolt", host="neo4j", port=7687, name=self.database_name )

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


def crate_nodes_and_relationship(graph, info, timestamp):
    # Создает из output_data первоначальный граф поиска

    for data_type, data in info['output_data']:
        # Создание
        new_node = Node(data_type, name=data)
        for parameter in info['input_parameters']:
            parent_node = Node(parameter['info_type'], name=parameter['data'])
            SERVICE = Relationship.type(info['service_info']['service_name'])
            graph.merge(SERVICE(parent_node, new_node), timestamp, "name")


#print(restart_neo4j())
# create_new_bd('neo4js')
# restart_neo4j()

# bson==0.5.8
n = Neo4jGraph('neo4jj')
n.pri()
n.delete_bd()