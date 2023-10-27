from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Доступ разрешен только администратору или суперпользователю."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser)


class IsOwnerOrAdminOnly(AdminOnly):
    """Доступ разрешен только владельцу или администратору
     с суперпользователем."""

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username or (
            super().has_object_permission())
