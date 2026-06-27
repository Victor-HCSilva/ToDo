from django.urls import path

from checklist.views import checklist

urlpatterns = [path("", checklist, name="checklist-form")]
