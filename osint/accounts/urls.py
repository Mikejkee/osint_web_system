from django.urls import path
from django.contrib.auth import views
from .forms import UserLoginForm

# TODO: Сделать регистрацию новых пользователей (если будет нужна)
# Пока новые пользователи через "mange.py createsuperuser" docker_app

urlpatterns = [
    path('login/', views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
