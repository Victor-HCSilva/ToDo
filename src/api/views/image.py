from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions.image import IsImageOwner
from api.serializers.image import ImageSerializer
from main.models import Image, Todo


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsImageOwner]

    def get_queryset(self):
        return Image.objects.filter(
            todo__in=Todo.objects.para_usuario(self.request.user),
            todo__is_active=True,
        ).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()
