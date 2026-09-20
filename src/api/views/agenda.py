from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from agenda.models import AgendaModel, Colors
from api.permissions.agenda import IsAgendaOwner
from api.serializers.agenda import AgendaModelSerializer, ColorsSerializer


class ColorsViewSet(viewsets.ModelViewSet):
    serializer_class = ColorsSerializer
    permission_classes = [IsAuthenticated, IsAgendaOwner]

    def get_queryset(self):
        return Colors.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AgendaModelViewSet(viewsets.ModelViewSet):
    serializer_class = AgendaModelSerializer
    permission_classes = [IsAuthenticated, IsAgendaOwner]

    def get_queryset(self):
        return AgendaModel.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
