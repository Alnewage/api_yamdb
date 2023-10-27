from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly, IsOwnerAdminModeratorOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer)
from api.utils import TitleFilter
from reviews.models import Category, Comment, Genre, Review, Title
from users.permissions import AdminOnly


class MethodPutDeniedMixin:
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed("Method PUT not allowed for this resource.")
        return super().update(request, *args, **kwargs)


class CategoryMixin:
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreMixin:
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(MethodPutDeniedMixin,
                   viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = IsAdminOrReadOnly,


class BaseCategoryGenreViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin):
    queryset = None
    serializer_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = IsAdminOrReadOnly,

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(BaseCategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(MethodPutDeniedMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    lookup_url_kwarg = 'review_id'
    permission_classes = IsOwnerAdminModeratorOrReadOnly,

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()


class CommentViewSet(MethodPutDeniedMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = IsOwnerAdminModeratorOrReadOnly,

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review=review)
