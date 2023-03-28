from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in ['GET', 'retrieve']
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Доступ запрещен!'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_staff
            or request.user.is_superuser
        )
