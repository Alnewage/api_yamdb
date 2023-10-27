import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework import serializers

User = get_user_model()


class ValidateUsernameMixin:
    """Миксин валидации имени пользователя."""

    @staticmethod
    def validate_username(value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Username must contain only letters, numbers,"
                " and characters .@+-")
        if value == 'me':
            raise ValidationError("Username 'me' is not allowed.")
        return value


class TokenSerializer(serializers.Serializer):
    """Serializer для токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class RegistrationSerializer(ValidateUsernameMixin, serializers.Serializer):
    """Serializer для регистрации пользователей."""

    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if User.objects.filter(email=email).exists() and not user:
            raise ValidationError({"email": "Email already exists."})
        if user and user.email != email:
            raise ValidationError({"email": "Email incorrect."})

        return data


class UserProfileSerializer(ValidateUsernameMixin,
                            serializers.ModelSerializer):
    """Serializer для профиля пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',)

    def validate_role(self, value):
        user = self.context['request'].user
        if user.role == 'admin' or user.is_superuser:
            return value
        raise serializers.ValidationError(
            "You don't have permission to change the role of this user.")
