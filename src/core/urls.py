from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ToDo API",
        default_version="v1",
        description=(
            "Documentação da API do projeto ToDo, incluindo tarefas, pastas, "
            "grupos, checklist, agenda e imagens."
        ),
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="contato@example.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="main:login", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/", include(("api.urls", "api"), namespace="api")),
    path("main/", include("main.urls")),
    path("agenda/", include("agenda.urls")),
    path("checklist/", include("checklist.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
    path("openapi.json", schema_view.without_ui(cache_timeout=0), name="schema"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
