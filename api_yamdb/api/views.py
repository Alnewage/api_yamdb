import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.exceptions import MethodNotAllowed
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


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(field_name='name')
    year = django_filters.NumberFilter(field_name='year')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),
        return AdminOnly(),

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed("Method PUT not allowed for this resource.")

        return super().update(request, *args, **kwargs)


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
