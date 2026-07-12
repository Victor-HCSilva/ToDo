from django.contrib import admin

from . import models

[admin.site.register(model) for model in [models.AgendaModel, models.Colors]]
