from rest_framework.authtoken.models import Token


def has_permissions(request, owner_token):
    token = request.auth or Token.objects.get(
        user=request.user).key

    return request.user.is_staff or token == owner_token
