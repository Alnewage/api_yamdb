from rest_framework import permissions


class AllowAnyOnlyList(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return False
