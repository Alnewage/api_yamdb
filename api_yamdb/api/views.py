from django.shortcuts import render
from django.shortcuts import get_object_or_404

from api.serializers import TitleSerializer, CategorySerializer, GenreSerializer
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Title, Category, Genre


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny, )

    def perform_create(self, serializer):
        serializer.save(rating=0)

    permission_classes = (permissions.AllowAny, )

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny, )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class =GenreSerializer
    permission_classes = (permissions.AllowAny, )
