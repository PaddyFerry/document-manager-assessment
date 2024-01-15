from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
        ]
        # fields = "__all__"

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        # }
