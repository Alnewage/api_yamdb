from django.core.cache import cache
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.exceptions import MethodNotAllowed

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsOwnerAdminModeratorOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Review, Title


class MethodPutDeniedMixin:
    """Миксин для запрета обновления ресурса с помощью PUT."""

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed("Method PUT not allowed for this resource.")
        return super().update(request, *args, **kwargs)


class TitleViewSet(MethodPutDeniedMixin,
                   viewsets.ModelViewSet):
    """Вьюсет модели Title."""

    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """Метод для получения QuerySet, аннотированного рейтингом."""
        queryset = Title.objects.annotate(avg_rating=Avg('reviews__score'))
        return queryset


class BaseCategoryGenreViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Базовый вьюсет для модели Category и Genre."""

    queryset = None
    serializer_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(BaseCategoryGenreViewSet):
    """Вьюсет модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCategoryGenreViewSet):
    """Вьюсет модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(MethodPutDeniedMixin, viewsets.ModelViewSet):
    """Вьюсет модели Review."""

    serializer_class = ReviewSerializer
    lookup_url_kwarg = 'review_id'
    permission_classes = IsOwnerAdminModeratorOrReadOnly,

    def get_title(self):
        title_id = self.kwargs.get('title_id')

        # Формирование ключа для кеширования
        cache_key = f"title_{title_id}"

        # Проверка наличия данных в кеше
        title = cache.get(cache_key)
        if title is None:
            # Если данных в кеше нет, получаем и сохраняем их
            title = get_object_or_404(Title, pk=title_id)
            cache.set(cache_key, title,
                      timeout=900)  # Сохранение данных в кеше на 15 минут

        return title

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()


class CommentViewSet(MethodPutDeniedMixin, viewsets.ModelViewSet):
    """Вьюсет модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = IsOwnerAdminModeratorOrReadOnly,

    def get_title_and_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')

        # Проверка кеша для получения данных
        cache_key = f"title_review_cache_{title_id}_{review_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # Если данные не найдены в кеше, получаем и сохраняем их
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, id=review_id, title=title)

        # Сохраняем данные в кеше на 15 минут.
        cache.set(cache_key, (title, review), timeout=900)
        return title, review

    def perform_create(self, serializer):
        title, review = self.get_title_and_review()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        _, review = self.get_title_and_review()
        return review.comments.all()
