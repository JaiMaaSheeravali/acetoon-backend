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


class IsOrganizer(permissions.BasePermission):
    """
    Allow Access to Organizers only
    """

    def has_permission(self, request, view):
        if hasattr(request.user, 'user'):

            return request.user.user.is_organizer

        return False


class AnnouncementPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method == 'POST':
            if hasattr(request.user, 'user'):
                return request.user.user == obj.contest.organizer
            else:
                return False
