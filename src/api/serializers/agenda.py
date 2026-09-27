from rest_framework import serializers

from agenda.models import AgendaModel, Colors, Reminder


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ["user", "cor_de_destaque", "cor_do_dia"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ["descricao", "agenda"]

    def create(self, validated_data):
        request = self.context["request"]
        return super().create(validated_data)





class AgendaModelSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AgendaModel
        fields = [
            "id",
            "user",
            "titulo",
            "descricao",
            "tipo_de_evento",
            "importancia",
            "dia_do_evento",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at", "is_active"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)
