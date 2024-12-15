from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.models import UserProfile
from user_profile.serializer import UserLoginSerializer, UserProfileSerializer

from .authentication import get_tokens_for_user
from .permissions import IsOwnerOrAdmin


class Home(APIView):
    def get(self, request):
        return Response({"message": "Health Check! True"})


class CreateUserProfile(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_data = UserProfile.objects.all()
        serialize_user_data = UserProfileSerializer(user_data, many=True)
        return Response(
            {
                "message": "Registered User List",
                "data": serialize_user_data.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serialize_data = UserProfileSerializer(data=request.data)
        serialize_data.is_valid(raise_exception=True)
        serialize_data.save()
        return Response(
            {
                "message": "User Register Successfully",
                "data": serialize_data.data
            },
            status=status.HTTP_201_CREATED
        )


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(
            {
                "message": "User Logged in Successfully",
                "user_email": str(user),
                **get_tokens_for_user(user)
            },
            status=status.HTTP_200_OK
        )


class ManageUserProfile(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def put(self, request):
        self.check_object_permissions(request=request, obj=None)

        user_data = UserProfile.objects.filter(
            email=request.data['email']
        ).first()

        serializer = UserProfileSerializer(user_data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "User modified Successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, user_id=None):
        self.check_object_permissions(request=request, obj=None)

        if user_id:
            user_data = UserProfile.objects.filter(user_id=user_id).first()
        else:
            user_data = UserProfile.objects.filter(
                email=request.data['email']
            ).first()
            user_id = user_data.user_id
        user_data.delete()
        return Response(
            {
                "message": "User deleted Successfully",
                "data": user_id
            },
            status=status.HTTP_200_OK
        )
