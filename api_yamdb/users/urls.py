from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (RegistrationViewSet, TokenViewSet, UserProfileMeView,
                    UserProfileViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'auth/token', TokenViewSet, basename='token')
router_v1.register(r'auth/signup', RegistrationViewSet, basename='registration')
router_v1.register(r'users', UserProfileViewSet, basename='user')

urlpatterns = [
    path('users/me/', UserProfileMeView.as_view(), name='me'),
    path('', include(router_v1.urls)),
]
