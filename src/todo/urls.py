from django.urls import path
from . import views
from home import views as views_init
from django.contrib.auth import views as auth_views

app_name = "main"

urlpatterns = [
    path(
        "login/",
        views_init.CustomLoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page=f"{app_name}:login"),
        name="logout",
    ),
    path(f"{app_name}/<int:id_user>", views_init.create_todo, name=f"{app_name}"),
    path("welcome/<int:id_user>", views_init.welcome, name="welcome"),
    path("sobre", views_init.sobre, name="sobre"),
    # ----------------------------------------------------
    path("editar/<int:id_user>/<int:id_anotacao>", views.editar, name="editar"),
    path("remover/<int:id_user>/<int:id_anotacao>", views.remover, name="remover"),
    path("anotacoes/<int:id_user>", views.anotacoes, name="anotacoes"),
    path("show/<int:id_user>/<int:id_anotacao>", views.show, name="show"),
    path(
        "apagar_imagem/<int:id_user>/<int:id_anotacao>/<int:id_imagem>",
        views.apagar_imagem,
        name="apagar_imagem",
    ),
    path(
        "editar_descricao/<int:id_user>/<int:id_anotacao>/<int:id_imagem>",
        views.editar_descricao,
        name="editar_descricao",
    ),
    path("not_found", views.not_found, name="404"),
]
