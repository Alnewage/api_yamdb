from django.shortcuts import render

# Create your views here.
from api.serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer,
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
    serializer_class = TitleSerializer
    # permission_classes = (AdminPermission,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method == 'get':
            return (permissions.AllowAny(), )
        return (permissions.AllowAny(), )


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