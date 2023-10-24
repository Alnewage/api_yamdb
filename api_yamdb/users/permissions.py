from rest_framework import permissions


class IsOwnerOrAdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user or request.user.role == 'admin'


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
