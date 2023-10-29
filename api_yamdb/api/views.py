from django.shortcuts import render

# Create your views here.
from api.serializers import (
    TitleReadSerializer, TitleCreateSerializer, CategorySerializer, GenreSerializer,
)
from api.permissions import (
    AdminPermission, ModeratorPermission, UserPermission,
)
from rest_framework import viewsets, permissions, filters
from reviews.models import Title, Category, Genre
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend


class CreateListDestroy(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)
    

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleCreateSerializer
    # permission_classes = (AdminPermission,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', 'genre__slug')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TitleCreateSerializer
        return TitleReadSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.AllowAny(), )
        return (AdminPermission(), )


class CategoryViewSet(CreateListDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'slug'
    

class GenreViewSet(CreateListDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'slug'