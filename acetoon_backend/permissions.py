from rest_framework import permissions


class AdminOnlyPermissions(permissions.BasePermission):
    """
    Allow access to admin only
    """

    def has_permission(self, request, view):

        return request.user.is_superuser


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow access to Admin or Requested User
    """

    def has_object_permission(self, request, view, obj):

        return request.user.is_superuser or request.user.id == obj.user.id
