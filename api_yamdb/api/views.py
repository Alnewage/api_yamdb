from rest_framework import mixins, permissions, viewsets, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView, DestroyAPIView
from rest_framework.viewsets import GenericViewSet

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title
from users.permissions import AdminOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny, )
    http_method_names = ['get', 'post', 'patch', 'delete', ]


class CategoryViewSet(ListCreateAPIView, DestroyAPIView, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        return (AdminOnly(), )


class GenreViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.AllowAny, )
