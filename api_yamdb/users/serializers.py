import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if not re.match(r'^[\w.@+-]+$', username):
            raise serializers.ValidationError(
                "Username must contain only letters,"
                " numbers, and characters .@+-")
        if username == 'me':
            raise ValidationError(
                {"username": "Username 'me' is not allowed."})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if User.objects.filter(email=email).exists() and not user:
            raise ValidationError({"email": "Email already exists."})
        if user and user.email != email:
            raise ValidationError({"email": "Email incorrect."})
        return data


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        read_only_fields = ('role',)

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Username must contain only letters,"
                " numbers, and characters .@+-")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',)

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Username must contain only letters,"
                " numbers, and characters .@+-")
        return value
