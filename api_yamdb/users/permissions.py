from rest_framework import permissions
"""IsAdminUser, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsModerator, AllowAny"""

# class ReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.method in permissions.SAFE_METHODS
#     def has_object_permission(self, request, view, obj):
#         return request.method in permissions.SAFE_METHODS


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)