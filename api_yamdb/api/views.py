from api.serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer,
)
from rest_framework import viewsets, permissions
from reviews.models import Title, Category, Genre
from rest_framework import mixins


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny, )
    http_method_names = ['get', 'post', 'patch', 'delete', ]


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny, )


class GenreViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.AllowAny, )
