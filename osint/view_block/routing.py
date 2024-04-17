from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("view/", consumers.TaskConsumer),
    path("search/", consumers.TaskConsumer)
]