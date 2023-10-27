from django.urls import include, path

from rest_framework import routers

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles',
                   TitleViewSet,
                   basename="titles")
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/'
                   r'(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')
router_v1.register(r'categories',
                   CategoryViewSet,
                   basename='categories')
router_v1.register(r'genres',
                   GenreViewSet,
                   basename='genres')

urlpatterns = [
    path('', include(router_v1.urls))
]
