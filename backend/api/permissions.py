from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import permissions


class IsAuthorOrReadOnly(BasePermission):
    def had_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def had_object_permission(self, request, view, obj):
        return obj.author == request.user or request.method in SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Доступ запрещен!'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )
