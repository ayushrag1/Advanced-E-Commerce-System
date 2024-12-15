from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh.payload['email'] = user.email
    refresh.payload['user_name'] = user.name
    refresh.payload['is_active'] = user.is_active
    refresh.payload['is_staff'] = user.is_staff
    refresh.payload['is_superuser'] = user.is_superuser
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
