from django.urls import path, re_path
# from .views import ViewPage, SearchFormView, PersonView, GroupView
from .views import SearchFormView, PersonView, GroupView
from .views import index

urlpatterns = [
    path('', index, name='view'),
    # path('', ViewPage.as_view(), name='view'),
    path('search_form/', SearchFormView.as_view(), name='search_form'),
    path('person/<str:pk>', PersonView.as_view(), name='person'),
    path('group/<str:label>', GroupView.as_view(), name='group'),
    # path('/search', post_search),
    # re_path(r'/person/(?P<person_id>.+)', person),
]