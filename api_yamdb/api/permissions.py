from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'moderator'


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        self.message = 'Необходимо авторизоваться'
        return (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        self.message = 'Доступно только автору'
        return (
            request.user and request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role == 'moderator'
            )
        )
