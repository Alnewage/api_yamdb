from api.views import TitleViewSet, CategoryViewSet, GenreViewSet
from rest_framework import routers
from django.urls import include, path


router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename="titles")
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('api/v1/', include(router_v1.urls))
]
