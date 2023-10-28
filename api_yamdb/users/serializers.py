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

        # Проверяем существует ли пользователь.
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        # Проверяем существует ли пользователь с таким email
        try:
            user_with_email = User.objects.get(email=email)
        except User.DoesNotExist:
            user_with_email = None

        # Если оба пользователя существуют и они не равны:
        if user and user_with_email and user != user_with_email:
            raise ValidationError({"username": "User already exists.",
                                   "email": "Email already exists."})

        # Если email уже используется, а само пользователь не существует:
        if user_with_email and not user:
            raise ValidationError({"email": "Email already exists."})

        # Если пользователь существует, но указанный email не его:
        if user and user.email != email:
            raise ValidationError({"username": "User already exists."})

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

    def validate(self, data):
        if self.context['request'].method in ['PATCH', 'POST']:
            if 'username' in data and not data['username']:
                raise serializers.ValidationError(
                    {"username": "This field is required."})
            if 'email' in data and not data['email']:
                raise serializers.ValidationError(
                    {"email": "This field is required."})
        return data
