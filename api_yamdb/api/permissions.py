from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
        
        def has_permission(self, request, view):
                return (request.method in permissions.SAFE_METHODS or
                        request.user.is_authenticated)
        
        def has_object_permission(self, request, view, obj):
                return (not request.user.is_anonymous)


class ModeratorPermission(permissions.BasePermission):
        pass


class UserPermission(permissions.BasePermission):
        pass