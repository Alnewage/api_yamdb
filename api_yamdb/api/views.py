from rest_framework import filters, permissions, viewsets
from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.viewsets import GenericViewSet

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title
from users.permissions import AdminOnly


class PermissionsMixin:
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),
        return AdminOnly(),


class CategoryMixin:
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreMixin:
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),
        return AdminOnly(),


class CategoryListCreateAPIView(CategoryMixin, PermissionsMixin,
                                ListCreateAPIView,
                                GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryDestroyAPIView(CategoryMixin, DestroyAPIView, GenericViewSet):
    lookup_field = 'slug'
    permission_classes = AdminOnly,


class GenreListCreateAPIView(GenreMixin, PermissionsMixin, ListCreateAPIView,
                             GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreDestroyAPIView(GenreMixin, DestroyAPIView, GenericViewSet):
    lookup_field = 'slug'
    permission_classes = AdminOnly,
