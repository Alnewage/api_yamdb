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


class CreateListRetriveView(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)
    

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(CreateListRetriveView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermission,)
    # def get_permissions(self):
    #     if not self.action == 'get':
    #         return (AdminPermission(),)
    #     return (permissions.IsAuthenticatedOrReadOnly(),)


class GenreViewSet(CreateListRetriveView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
