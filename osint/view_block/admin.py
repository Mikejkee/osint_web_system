from django.contrib import admin
from .models import Person, Document


admin.site.register([Person, Document])