from rest_framework import serializers

from main.models import Folder, Todo


class FolderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Folder
        fields = [
            "id",
            "name",
            "user",
            "colaboradores",
            "grupos_colaboracao",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "user",
            "colaboradores",
            "grupos_colaboracao",
            "is_active",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    folder = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Todo
        fields = [
            "id",
            "user",
            "titulo",
            "favorito",
            "completo",
            "anotacao",
            "prioridade",
            "tag",
            "prazo_inicial",
            "prazo_final",
            "folder",
            "colaboradores",
            "grupos_colaboracao",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "user",
            "colaboradores",
            "grupos_colaboracao",
            "created_at",
            "updated_at",
            "is_active",
        ]

    def validate_folder(self, value):
        request = self.context["request"]
        if value is None:
            return value
        if value.user != request.user and not value.pode_editar(request.user):
            raise serializers.ValidationError(
                "Você não tem permissão para usar esta pasta."
            )
        return value

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)
