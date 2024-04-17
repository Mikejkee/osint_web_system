from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging
import json

from osint.celery import app
from .models import Task
from utils.services_functions import format_datetime
from utils.smart_import import get_service_functions
from utils.smart_chain import get_chains_function

channel_layer = get_channel_layer()
logger = logging.getLogger()


@app.task
def task_function(search_timestamp, search_type, search_value, search_name):
    # Отправка в сервис и получение результата
    if search_type == 'service':
        service_result = get_service_functions(search_type, search_name, search_value)
        print(service_result)
    elif search_type == 'chain':
        print(search_name)
        service_result = get_chains_function(search_name, search_value)
    # Коннеккт к neo4j
    #graph = Graph(scheme="bolt", host="neo4j", port=7687)

    # Создание графа поиска
    #crate_nodes_and_relationship(graph, service_result, search_timestamp)

    # Изменение статуса таски на выполненную
    task = Task.objects.get(search_timestamp=search_timestamp)
    task.status = "completed"
    task.save()

    response = {
        "action": "completed",
        "task_created": format_datetime(task.created),
        "task_id": task.id,
        "task_name": task.search_value,
        "task_status": task.status,
        "service_result": service_result,
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "taskstatus",
        {
            "type": "update.task",
            "text": json.dumps(response),
        },
    )


#def crate_nodes_and_relationship(graph, info, timestamp):
#    # Создает из output_data первоначальный граф поиска
#    for data_type, data in info['output_data']:
#        # Создание  
#        new_node = Node(data_type, name=data)
#        for parameter in info['input_parameters']:
#            parent_node = Node(parameter['info_type'], name=parameter['data'])
#            SERVICE = Relationship.type(info['service_info']['service_name'])
#            graph.merge(SERVICE(parent_node, new_node), timestamp, "name")


# def docker_up(timestamp):
#     path = './search_result/' + timestamp + "/"
#     try:
#         mkdir(path)
#     except:
#         pass
#
#     cli = docker.APIClient(base_url='unix:///var/run/docker.sock')
#     container_id = cli.create_container(
#         image='neo4j',
#         # volumes=['d:/Ucheba/fourthsem/Sorokin/pythonProjects/docker/neo4j/data/'],
#         ports=[7474, 7687],
#         name=timestamp,
#         host_config=cli.create_host_config(
#             privileged=True,
#             binds=[
#                 path + 'data/:/data',
#             ],
#             port_bindings={
#                 7474: 7474,
#                 7687: 7687,
#             }
#         ),
#         environment=["NEO4J_AUTH=neo4j/123123"],
#     )
#     cli.start(container=container_id.get('Id'))
#     return path



# docker run -d -p 6379:6379 redis             - докер для запуска redisa
# celery -A osint worker -l info -P eventlet   - команда запуска celery (в отдельном окне терминала надо)
# celery -A osint worker -l debug -P eventlet  - в режиме дебаг
# celery -A osint beat -l info                 - запуск shared task (в отдельном окне терминала надо)
# celery -A osint purge -f                      - отчистить очередь
# flower -A osint --port=5555                   - запуск flower для отслеживания заданий в вебе (в отдельном окне терминала надо)



# @shared_task
# def get_random_joke():
#     res = requests.get("http://api.icndb.com/jokes/random").json()
#     joke = res["value"]["joke"]
#     logger.info('Шутка: '+joke + '   ' + str(channel_layer))
#     # Передаем сообщение типа `view.joke` через channel_layer
#     # всем потребителям, которые подключены к группе `view`.
#     async_to_sync(channel_layer.group_send)(
#         "view", {"type": "view.joke", "text": joke}
#     )
#     print('PEREDAL')