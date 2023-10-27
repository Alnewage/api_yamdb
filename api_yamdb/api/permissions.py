from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для остальных методов, пользователь должен быть аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Проверяем, что пользователь является владельцем или
        # имеет роль "admin" или "moderator".
        return any([obj.author == request.user,
                    request.user.role in ['admin', 'moderator'], ])
