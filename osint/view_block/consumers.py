from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from time import time, sleep
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Task
from .tasks import task_function
from utils.services_functions import format_datetime
import logging


logger = logging.getLogger(__name__)


class TaskConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)

        layer_identifier = "taskstatus"
        self.layer_identifier = layer_identifier
        await self.channel_layer.group_add(layer_identifier, self.channel_name)

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        await self.channel_layer.group_discard(self.layer_identifier, self.channel_name)

    async def websocket_receive(self, event):
        print("receive", event)
        receive_message = event.get('text', None)

        if receive_message is not None:
            # Подгружаем то, что пришло, десериализируем его
            loaded_data = json.loads(receive_message)

            # Идем по каждому запросу и формируем таски для каждого сервиса
            for search_query in loaded_data:
                # Сохаранение нового задания в бд
                str_value = ""
                for search_value in search_query['search_parameters']:
                    str_value += search_query['search_parameters'][search_value] + ", "
                new_task = await self.create_new_task(str(time()), search_query['search_type'],
                                                      search_query['service_name'], str_value)

                # Формирует ответ для отправки назад
                response = {
                    "action": "started",
                    "task_created": format_datetime(new_task.created),
                    "task_id": new_task.id,
                    "task_type": new_task.search_type,
                    "task_name": new_task.search_value,
                    "task_status": "started",
                }

                # Задержка т.к. сессий в телеге 2, если много запросов - не работало, когда будет много сессий - убрать
                sleep(1)
                logger.info(msg='QUERY BY USER - "{}"; SERVICE - "{}"  :  {}'.format(search_query['userName'],
                                                                                     new_task.search_type,
                                                                                     search_query['search_parameters']))
                task_function.delay(new_task.search_timestamp, new_task.search_type, search_query['search_parameters'],
                                    new_task.search_name)

                # Отпрака обратного сообщения о начале выполняения
                await self.channel_layer.group_send(
                    self.layer_identifier,
                    {
                        "type": "new.object",
                        "text": json.dumps(response),
                    },
                )

    async def new_object(self, event):
        # Send message
        await self.send({
            'type': "websocket.send",
            'text': event['text']
        })

    async def update_task(self, task):
        # Обновление статуса задания
        print(task['text'])
        await self.send({
            'type': "websocket.send",
            'text': task['text']
        })

    @database_sync_to_async
    def create_new_task(self, search_timestamp, search_type, search_name, search_value):
        return Task.objects.create(
            search_timestamp=search_timestamp,
            search_type=search_type,
            search_name=search_name,
            search_value=search_value,
            status="started",
        )



# class JokesConsumer(WebsocketConsumer):
#     def connect(self):
#         # Подключает канал с именем `self.channel_name`
#         # к группе `view`
#         print("CONN")
#         async_to_sync(self.channel_layer.group_add)(
#             "view", self.channel_name
#         )
#         # Принимает соединение
#         self.accept()
#
#     def disconnect(self, close_code):
#         # Отключает канал с именем `self.channel_name`
#         # от группы `view`
#         print('DISC')
#         async_to_sync(self.channel_layer.group_discard)(
#             "view", self.channel_name
#         )
#
#     # Метод `jokes_joke` - обработчик события `view.joke`
#     def view_joke(self, event):
#         # Отправляет сообщение по вебсокету
#         print("SEND")
#         self.send(text_data=event["text"])