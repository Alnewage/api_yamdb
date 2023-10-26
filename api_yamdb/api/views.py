from rest_framework import filters, permissions, viewsets
from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.viewsets import GenericViewSet

from api.permissions import AllowAnyOnlyList
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title
from users.permissions import AdminOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny, )
    http_method_names = ['get', 'post', 'patch', 'delete', ]


class CategoryListCreateAPIView(ListCreateAPIView, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),
        return AdminOnly(),


class CategoryDestroyAPIView(DestroyAPIView, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = AdminOnly,


class GenreListCreateAPIView(ListCreateAPIView, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return AllowAnyOnlyList(),
        return AdminOnly(),


class GenreDestroyAPIView(DestroyAPIView, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = AdminOnly,
