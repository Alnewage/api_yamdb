from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (RegistrationViewSet, TokenViewSet, UserProfileUpdateView,
                    UserProfileViewSet)

router = DefaultRouter()
router.register(r'auth/token', TokenViewSet, basename='token')
router.register(r'auth/signup', RegistrationViewSet, basename='registration')
router.register(r'users', UserProfileViewSet, basename='user')

urlpatterns = [
    path('users/me/', UserProfileUpdateView.as_view(), name='me'),
    path('', include(router.urls)),
]
