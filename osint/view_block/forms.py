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


class SearchForm(forms.Form):
    name = forms.CharField(label='Имя',
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'input--style-1 input-sf',
                                   'type': 'text',
                                   'placeholder': "Имя",
                               }))
    surname = forms.CharField(label='Фамилия',
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'input--style-1 input-sf',
                                      'type': 'text',
                                      'placeholder': "Фамилия",
                                  }))
    patronymic = forms.CharField(label='Отчество',
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'input--style-1 input-sf',
                                   'type': 'text',
                                   'placeholder': "Отчество",
                                      }))
    birth_date = forms.DateField(label='Дата рождения',
                           widget=TextInput(
                               attrs={
                                   'class': 'input--style-1 input-sf daterange',
                                   'type': 'text',
                                   'placeholder': "Дата рождения",
                                      }), required=False)
