from django.shortcuts import render, reverse
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.db.models import Q
from .forms import SearchForm
from .models import Person, Task
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.template import loader
from pprint import pprint


# 173, 195, 202


def index(request):
    # Get objects from database
    tasks = Task.objects.all()

    context = {
        'tasks': tasks,
    }

    return render(request, 'view_block/view.html', context)




# class ViewPage(TemplateView):
#     template_name = 'view_block/view.html'
#
#
class SearchFormView(FormView):
    template_name = 'view_block/post_search.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        # Ищем в базе по какому-то полю айдишник (пока так)
        # TODO: Определиться по каким полям и как будет осуществляться поиск
        try:
            id_searched_person = Person.objects.filter(main_info={'surname': self.object.cleaned_data['surname']})
        except IndexError:
            id_searched_person = 0
        # Если несколькло результатов то перекидываем на групповой просмотр
        if len(id_searched_person) == 1:
            return reverse('person', kwargs={'pk': str(id_searched_person[0]._id)})
        else:
            self.request.session['search_group_ids'] = []
            for id in id_searched_person:
                if 'search_group_ids' not in self.request.session['search_group_ids']:
                    self.request.session['search_group_ids'].append(str(id._id))
            return reverse('group', kwargs={'label': 'search_group'})

class PersonView(DetailView):
    model = Person
    template_name = 'view_block/person.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person_info = model_to_dict(super().get_object())
        # for dict_element in person_info:
        #     if dict_element != '_id' and dict_element != 'documents':
        #         if type(person_info[dict_element]) == list:
        #             for index in range(0, len(person_info[dict_element])):
        #                 person_info[dict_element][index] = model_to_dict(person_info[dict_element][index])
        #         else:
        #             person_info[dict_element] = model_to_dict(person_info[dict_element])
        # print(person_info)
        context['person'] = person_info
        return context


class GroupView(ListView):
    model = Person
    template_name = 'view_block/group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['search_group_ids']
        search_group_list = []
        for id in self.request.session['search_group_ids']:
            search_group_list.append(Person.objects.get(_id=id))
        context['group'] = search_group_list
        return context


class SearchResultsView(ListView):
    model = Person
    template_name = 'view_block/person.html'

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        object_list = Person.objects.filter(
            Q(name__icontains=query)
        )
        return object_list


# def index(request):
#     return render(request, 'view_block/view.html', {})
#
# def post_search(request):
#     if request.method == 'POST':
#         print(request.POST)
#         search_form = SearchForm(request.POST)
#         if search_form.is_valid():
#             name = search_form.cleaned_data['name']
#             patronymic = search_form.cleaned_data['patronymic']
#             surname = search_form.cleaned_data['surname']
#             birth_date = search_form.cleaned_data['birth_date']
#             print({name, surname, patronymic, birth_date})
#             print('DA')
#             searched_person = Person.objects.get(main_info={'name': name})
#             # return render(request, 'view_block/person.html', {'person': {'name': 'Mike', "surname": 'Mosin'}})
#             person(request, searched_person._id)
#         else:
#             print('NET')
#             pprint(search_form.errors)
#     else:
#         search_form = SearchForm()
#         return render(request, "view_block/post_search.html", {"form": search_form})
#
#
# def person(request, person_id):
#     searched_person = Person.objects.get(_id=person_id)
#     print(searched_person)
#     return render(request, 'view_block/person.html', {"results": ""})
