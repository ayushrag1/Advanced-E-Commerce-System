from rest_framework.permissions import SAFE_METHODS, BasePermission

from ..utils import logging_entry_exit


class IsOwnerOrAdmin(BasePermission):
    """
    Permission class that allows access to:
    - Superusers (admins) for any action
    - Resource owners for their own resources
    """

    @logging_entry_exit
    def has_permission(self, request, view):
        """
        Check if user is authenticated and has basic permission to access this view.
        This is called before has_object_permission.
        """
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Superusers have full access
        if request.user.is_superuser:
            return True

        # Ensure token has user_id
        token_user_id = request.user.token.get('user_id')
        if token_user_id is None:
            return False

        # If there's no user_id in the URL, or if it matches the token's user_id
        view_user_id = view.kwargs.get('user_id')
        if view_user_id is None:
            return request.method in SAFE_METHODS

        return int(view_user_id) == int(token_user_id)

    @logging_entry_exit
    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to access the specific object.
        Only called if has_permission() returns True.
        """
        # Superusers have full access
        if request.user.is_superuser:
            return True

        view_user_id = view.kwargs.get('user_id')
        token_user_id = request.user.token.get('user_id')
        if token_user_id is None or view_user_id is None:
            return False

        if int(view_user_id) != token_user_id:
            return False

        # For write operations (POST, PUT, PATCH, DELETE) - validate email matches token
        else:
            # Safely check if provided email matches token email
            token_email = request.user.token.get('email')
            request_email = request.data.get('email') if request.data else None

            if request_email and token_email != request_email:
                return False

            return True
