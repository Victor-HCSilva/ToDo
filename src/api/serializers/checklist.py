from rest_framework import serializers

from checklist.models import Item, Link, Tarefa


class ItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "descricao",
            "feito",
            "color",
            "user",
            "tarefa",
            "is_active",
        ]
        read_only_fields = ["id", "user", "is_active"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)


class LinkSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Link
        fields = ["id", "url", "user", "tarefa", "is_active"]
        read_only_fields = ["id", "user", "is_active"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)


class TarefaSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    itens = ItemSerializer(many=True, read_only=True)
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Tarefa
        fields = ["id", "titulo", "color", "user", "is_active", "itens", "links"]
        read_only_fields = ["id", "user", "is_active"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)
