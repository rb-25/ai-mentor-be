from rest_framework import serializers

from gdg_be.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["interests", "experience"]
        read_only_fields = ["email", "name"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UpdateUserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["interests", "experience"]
        read_only_fields = ["email", "name"]
