import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import Http404
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

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        # Проверяем существует ли пользователь.
        user = User.objects.filter(username=username).first()

        # Если существует пользователь с таким кодом подтверждения:
        if user and user.confirmation_code == confirmation_code:
            return data

        # Если пользователь существует, но указанный код не совпадает:
        if user and user.confirmation_code != confirmation_code:
            raise ValidationError(
                {"confirmation_code": "Confirmation code is wrong."})
        # Значит такого пользователя нет.
        raise Http404("User does not exist.")


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
        user = User.objects.filter(username=username).first()

        # Проверяем существует ли пользователь с таким email.
        user_with_email = User.objects.filter(email=email).first()

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
            'username', 'email', 'role', 'first_name', 'last_name', 'bio')

    def validate_role(self, value):
        user = self.context['request'].user
        # Проверяем, является ли пользователь админом,
        # модератором или суперпользователем.
        if user.role in ['admin', 'moderator'] or user.is_superuser:
            return value
        # Иначе игнорируем роль и возвращаем уже установленную.
        return user.role

    def validate(self, data):
        if self.context['request'].method in ['PATCH', 'POST']:
            if 'username' in data and not data['username']:
                raise serializers.ValidationError(
                    {"username": "This field is required."})
            if 'email' in data and not data['email']:
                raise serializers.ValidationError(
                    {"email": "This field is required."})
        return data
