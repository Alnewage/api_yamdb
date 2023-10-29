from rest_framework import permissions


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Или метод безопасный или пользователь аутентифицирован.
        return request.method in permissions.SAFE_METHODS or (
            request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        # Или метод безопасный, или пользователь является владельцем,
        # или имеет роль "admin" или "moderator",
        # или он является суперпользователем.
        return request.method in permissions.SAFE_METHODS or (
            obj.author == user) or user.is_superuser or (
            user.role in [user.Role.ADMIN, user.Role.MODERATOR])


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        # Или метод безопасный или пользователь аутентифицирован
        # и имеет роль администратора или суперпользователя.
        return request.method in permissions.SAFE_METHODS or (
            user.is_authenticated and (
                user.role == user.Role.ADMIN or user.is_superuser))
