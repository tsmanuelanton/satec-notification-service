from rest_framework.authtoken.models import Token


def has_permissions(request, user):
    return request.user.is_staff or request.user == user
