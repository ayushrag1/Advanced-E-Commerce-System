from django.contrib.auth import authenticate
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        Serializer, ValidationError)

from .models import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'user_id', 'email', 'name', 'address',
            'phone', 'password', 'is_staff',
            'is_active', 'date_joined'
        )
        read_only_fields = (
            'user_id', 'is_staff', 'is_active', 'date_joined'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': True},
            'name': {'required': True},
            'phone': {'required': True},
            'address': {'required': True}
        }

    def create(self, validated_data):
        """
        Create and return a new UserProfile instance
        """
        password = validated_data.pop('password')
        user = UserProfile.objects.create_user(
            **validated_data,
            password=password
        )
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing UserProfile instance
        """
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance


class UserLoginSerializer(Serializer):
    email = EmailField(
        error_messages={
            'required': 'Email field is required.',
            'invalid': 'Enter a valid email address.'
        }
    )

    password = CharField(
        write_only=True,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Password field is required.'
        }
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Authenticate user
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        # Handle authentication failure
        if not user:
            raise ValidationError(
                detail={
                    'error': 'Incorrect Login credentials.'
                },
            )

        # Check if user is active
        if not user.is_active:
            raise ValidationError(
                detail={
                    'error': 'User account is disabled.'
                },
            )

        attrs['user'] = user
        return attrs
