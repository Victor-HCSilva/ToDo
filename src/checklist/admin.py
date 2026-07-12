from django.contrib import admin

from .models import Item, Link, Tarefa

# Register your models here.

[admin.site.register(model) for model in [Link, Item, Tarefa]]
