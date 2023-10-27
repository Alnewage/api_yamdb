from django.urls import include, path

from rest_framework import routers

from api.views import (CategoryDestroyAPIView, CategoryListCreateAPIView,
                       GenreDestroyAPIView, GenreListCreateAPIView,
                       ReviewViewSet, TitleViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles',
                   TitleViewSet,
                   basename="titles")
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'categories',
                   CategoryListCreateAPIView,
                   basename='categories')
router_v1.register(r'categories',
                   CategoryDestroyAPIView,
                   basename='categories-destroy')
router_v1.register(r'genres',
                   GenreListCreateAPIView,
                   basename='genres')
router_v1.register(r'genres',
                   GenreDestroyAPIView,
                   basename='genres-destroy')

urlpatterns = [
    path('', include(router_v1.urls))
]
