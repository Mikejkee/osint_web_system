from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.forms.widgets import Input, TextInput

class CustomInput(Input):
    def get_context(self, name, value, attrs):
        context = super(CustomInput, self).get_context(name, value, attrs)
        if context['widget']['attrs'].get('name') is not None:
            context['widget']['name'] = context['widget']['attrs']['name']
        return context


class CustomTextInput(TextInput, CustomInput):
    pass


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='Логин',
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'input--style-1 input-sf',
                                   'type': 'text',
                                   'placeholder': "Введите логин",
                               }))
    password = forms.CharField(label='Пароль',
                              widget=forms.PasswordInput(
                                  attrs={
                                      'class': 'input--style-1 input-sf',
                                      'type': 'password',
                                      'placeholder': "Введите пароль",
                                  }))