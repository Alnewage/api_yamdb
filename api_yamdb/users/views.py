from django.contrib.auth import get_user_model

from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AdminOnly, IsOwnerOrAdminOnly
from .serializers import (RegistrationSerializer, TokenSerializer,
                          UserProfileSerializer, UserProfileUpdateSerializer)
from .utils import get_confirmation_code, send_confirmation_code

User = get_user_model()


class RegistrationViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            confirmation_code = get_confirmation_code()

            # Сохраняем объект User.
            User.objects.create(
                username=username,
                email=email,
                confirmation_code=confirmation_code, )

            # Отправляем код подтверждения по электронной почте
            send_confirmation_code(email, username)

            # Возвращаем confirmation_code в ответе
            return Response({'confirmation_code': confirmation_code},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['post'])
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']

            try:
                user = User.objects.get(
                    username=username,
                    confirmation_code=confirmation_code)
            except User.DoesNotExist:
                return Response(
                    {'error': 'Неверное имя пользователя или'
                              ' код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return (AllowAny(),)
        return (IsOwnerOrAdminOnly(),)

    def get_object(self):
        return self.request.user


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AdminOnly,)
    lookup_field = 'username'
