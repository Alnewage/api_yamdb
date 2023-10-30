from django.contrib.auth import get_user_model

from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AdminOnly
from .serializers import (RegistrationSerializer, TokenSerializer,
                          UserProfileSerializer)
from .utils import get_confirmation_code, send_confirmation_code

User = get_user_model()


class AllowAnyMixin:
    """Миксин для разрешения любого пользователя."""

    permission_classes = (AllowAny,)


class UserProfileMixin:
    """Миксин для работы с профилем пользователя."""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class RegistrationViewSet(AllowAnyMixin, viewsets.ViewSet):
    """Вьюсет регистрации пользователя."""

    @staticmethod
    def create(request):
        serializer = RegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        # Делаем проверку, что существующий пользователь вторично
        # запрашивает свой код подтверждения.
        try:
            user = User.objects.get(username=username)
            if user.email == email:
                send_confirmation_code(email, username)
                return Response(
                    {'email': email, 'username': username},
                    status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        confirmation_code = get_confirmation_code()

        User.objects.create(username=username,
                            email=email,
                            confirmation_code=confirmation_code)

        # Отправляем код подтверждения по электронной почте
        send_confirmation_code(email, username)

        return Response(
            {'email': email, 'username': username, },
            status=status.HTTP_200_OK)


class TokenViewSet(AllowAnyMixin, viewsets.ViewSet):
    """Вьюсет токена."""

    @staticmethod
    def create(request):
        serializer = TokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        user = User.objects.get(username=username)
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)},
                        status=status.HTTP_200_OK)


class UserProfileMeView(UserProfileMixin, generics.RetrieveUpdateAPIView):
    """Вьюсет для работы с профилем пользователя для эндпоинта /me."""

    def get_object(self):
        return self.request.user


class UserProfileViewSet(UserProfileMixin, viewsets.ModelViewSet):
    """Вьюсет для работы с профилем пользователя."""

    permission_classes = (AdminOnly,)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed("Method PUT not allowed for this resource.")

        return super().update(request, *args, **kwargs)
