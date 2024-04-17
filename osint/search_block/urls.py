from django.urls import path
from .views import SearchPage, index, get_services, get_chains

urlpatterns = [
    # path('', SearchPage.as_view(), name='search'),
    path('', index, name='search'),
    path('get_services', get_services, name='get_services'),
    path('get_chains', get_chains, name='get_chains'),
]
