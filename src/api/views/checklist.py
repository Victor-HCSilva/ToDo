from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions.checklist import IsChecklistOwner
from api.serializers.checklist import ItemSerializer, LinkSerializer, TarefaSerializer
from checklist.models import Item, Link, Tarefa


class TarefaViewSet(viewsets.ModelViewSet):
    serializer_class = TarefaSerializer
    permission_classes = [IsAuthenticated, IsChecklistOwner]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Tarefa.objects.none()
        return Tarefa.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsChecklistOwner]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Item.objects.none()
        return Item.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated, IsChecklistOwner]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Link.objects.none()
        return Link.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
