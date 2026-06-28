from django.contrib import admin

# Register your models here.
from .models import Folder, Image, Todo

admin.site.register(Folder)
admin.site.register(Image)
admin.site.register(Todo)
