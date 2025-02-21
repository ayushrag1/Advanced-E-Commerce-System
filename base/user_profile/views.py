from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import get_tokens_for_user
from .models import UserProfile
from .permissions import IsOwnerOrAdmin
from .serializer import UserLoginSerializer, UserProfileSerializer


class Home(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Health Check! True"})


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling UserProfile operations:
    - Anyone can register (create)
    - Only admins can list all users
    - Users can view/edit their own profiles
    - Admins can view/edit any profile
    """
    serializer_class = UserProfileSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        """
        Restrict the queryset to only the user's own profile unless the user is a superuser.
        """
        user = self.request.user
        if user.is_superuser:
            return UserProfile.objects.all()  # Superusers can see all profiles
        return UserProfile.objects.filter(user_id=user.user_id)  # Normal users see only their own profile

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        print(f"{self.action=}")
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsOwnerOrAdmin]

        return [permission() for permission in permission_classes]


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                {
                    "message": "Login failed",
                    "errors": serializer.errors
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = serializer.validated_data['user']

        # Get tokens for user
        tokens = get_tokens_for_user(user)

        return Response(data={
            "message": "Login successful",
            "data": {
                "user": {
                        "email": user.email,
                        "name": user.name
                        },
                "tokens": tokens
            }
        },
            status=status.HTTP_200_OK
        )
