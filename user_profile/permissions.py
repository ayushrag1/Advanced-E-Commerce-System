from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = view.kwargs.get('user_id')
        # Make sure that an owner can only modify and access its own objects
        if request.user.is_superuser:
            return True  # Superuser can access anything

        if request.method in SAFE_METHODS:
            return True  # Allow safe methods (GET, HEAD, OPTIONS)

        # Check if the request user is the owner of the object
        user_id = view.kwargs.get('user_id')
        if user_id == request.user.token['user_id']:
            return True

        if request.data:
            return request.user.token['email'] == request.data['email']
        return False

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
