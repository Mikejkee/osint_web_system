from django.shortcuts import render, reverse
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils.datastructures import MultiValueDictKeyError
from .forms import SearchForm
from time import time, sleep
from os import mkdir
import docker
import json
import os
from py2neo import Graph, Node, Relationship


def get_services(request):
    dir = os.path.abspath(os.curdir)
    with open('./utils/services_info.json', "r", encoding='windows-1251') as read_file:
        service_info = json.load(read_file)
    return JsonResponse(service_info)


def get_chains(request):
    dir = os.path.abspath(os.curdir)
    with open('./utils/chains_info.json', "r", encoding='windows-1251') as read_file:
        service_info = json.load(read_file)
    return JsonResponse(service_info)


def index(request):
    return render(request,  'search_block/search.html')


def handle_uploaded_file(file, path):
    file_path = path + str(file)
    with open(file_path, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    return file_path


def crate_nodes_and_relationship(graph, info, timestamp):
    for node in info['data']:
        new_node = Node(node['type'], name=node['data'])
        for parent in info['input']:
            parent_node = Node(parent['type'], name=parent['data'])
            SERVICE = Relationship.type(info['service']['name'])
            graph.merge(SERVICE(parent_node, new_node), timestamp, "name")


def docker_up(timestamp):
    path = 'd:/Ucheba/fourthsem/Sorokin/pythonProjects/osint/osint/search_block/media/' + timestamp + "/"
    try:
        mkdir(path)
    except:
        pass

    cli = docker.APIClient(base_url='npipe:////./pipe/docker_engine')
    container_id = cli.create_container(
        image='neo4j',
        volumes=['d:/Ucheba/fourthsem/Sorokin/pythonProjects/docker/neo4j/data/'],
        ports=[7474, 7687],
        name=timestamp,
        host_config=cli.create_host_config(
            binds=[
                path + 'data/:/data',
            ],
            port_bindings={
                7474: 7474,
                7687: 7687,
            }
        ),
        environment=["NEO4J_AUTH=neo4j/123123"],
    )
    response = cli.start(container=container_id.get('Id'))
    return path


class SearchPage(TemplateView):
    template_name = 'search_block/search.html'
