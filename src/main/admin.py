from django.contrib import admin

from .models import Folder, Image, Todo

[admin.site.register(model) for model in [Folder, Image, Todo]]
