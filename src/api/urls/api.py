from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views.agenda import AgendaModelViewSet, ColorsViewSet
from api.views.auth import MeView
from api.views.checklist import ItemViewSet, LinkViewSet, TarefaViewSet
from api.views.group import GroupViewSet
from api.views.image import ImageViewSet
from api.views.todo import FolderViewSet, TodoViewSet

app_name = "api"

router = DefaultRouter()
router.register(r"todos", TodoViewSet, basename="todo")
router.register(r"folders", FolderViewSet, basename="folder")
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"checklist/tarefas", TarefaViewSet, basename="tarefa")
router.register(r"checklist/itens", ItemViewSet, basename="item")
router.register(r"checklist/links", LinkViewSet, basename="link")
router.register(r"agenda", AgendaModelViewSet, basename="agenda")
router.register(r"agenda/configs", ColorsViewSet, basename="colors")
router.register(r"images", ImageViewSet, basename="image")

urlpatterns = [
    path(
        "auth/",
        include(
            [
                path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
                path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
                path("me/", MeView.as_view(), name="me"),
            ]
        ),
    ),
    path("", include(router.urls)),
]
