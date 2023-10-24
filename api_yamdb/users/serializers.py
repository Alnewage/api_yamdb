from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        'username', 'email', 'first_name', 'last_name', 'bio', 'role',)
