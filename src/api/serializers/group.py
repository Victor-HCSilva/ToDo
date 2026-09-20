from django.contrib.auth import get_user_model
from rest_framework import serializers

from main.models import CollaborationGroup

User = get_user_model()


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSummarySerializer(read_only=True)
    membros = UserSummarySerializer(many=True, read_only=True)

    class Meta:
        model = CollaborationGroup
        fields = [
            "id",
            "name",
            "descricao",
            "owner",
            "membros",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "owner",
            "membros",
            "created_at",
            "updated_at",
            "is_active",
        ]


class GroupMemberSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user", queryset=User.objects.all()
    )


class ShareSerializer(serializers.Serializer):
    user_ids = serializers.PrimaryKeyRelatedField(
        source="users", queryset=User.objects.all(), many=True, required=False
    )
    group_ids = serializers.PrimaryKeyRelatedField(
        source="groups",
        queryset=CollaborationGroup.objects.filter(is_active=True),
        many=True,
        required=False,
    )

    def validate(self, attrs):
        if not attrs.get("users") and not attrs.get("groups"):
            raise serializers.ValidationError("Informe ao menos um usuário ou grupo.")
        return attrs
