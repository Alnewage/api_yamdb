from api.serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer,
)
from rest_framework import viewsets, permissions, filters
from reviews.models import Title, Category, Genre
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (permissions.AllowAny, )
    http_method_names = ['get', 'post', 'patch', 'delete', ]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
