from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Only the author (or a staff member) can edit a post."""

    def has_permission(self, request, view):
        # Anyone can read; only logged-in users can create.
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff
