from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="main:login", permanent=False)),
    path("admin/", admin.site.urls),
    path("main/", include("main.urls")),
    path("agenda/", include("agenda.urls")),
    path("checklist/", include("checklist.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
