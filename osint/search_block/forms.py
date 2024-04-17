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
                           required=False,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'type': 'text',
                                   'id': 'input_name',
                                   'onchange': 'checkSearchParams(this.id)',
                               }))
    surname = forms.CharField(label='Фамилия',
                              required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control',
                                      'type': 'text',
                                      'id': 'input_surname',
                                      'onchange': 'checkSearchParams(this.id)',
                                  }))
    email = forms.EmailField(label='Почта',
                             required=False,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'type': 'email',
                                     'id': 'input_email',
                                     'onchange': 'checkSearchParams(this.id)',
                                        }))
    photo = forms.ImageField(label='Фото',
                            required=False,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'type': 'file',
                                    'id': 'input_photo',
                                    'onchange': 'checkSearchParams(this.id)',
                                       }))
    # birth_date = forms.DateField(label='Дата рождения',
    #                        widget=TextInput(
    #                            attrs={
    #                                'class': 'input--style-1 input-sf daterange',
    #                                'type': 'text',
    #                                'placeholder': "Дата рождения",
    #                                   }), required=False)
