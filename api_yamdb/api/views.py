from django.shortcuts import get_object_or_404

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer)
from reviews.models import Category, Comment, Genre, Review, Title
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


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer
    lookup_url_kwarg = 'review_id'
    permission_classes = IsOwnerOrReadOnly,

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed("Method PUT not allowed for this resource.")

        return super().update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = IsOwnerOrReadOnly,

    def perform_create(self, serializer):
        """Создание нового коммента."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        """Получение кверисета."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review=review)
