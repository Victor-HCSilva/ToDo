from django.contrib import admin
from .models import User, Todo, Image


admin.site.register(Todo)
admin.site.register(Image)
