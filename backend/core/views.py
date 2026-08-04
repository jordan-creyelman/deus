from django.db import connection
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """Crée un compte utilisateur sans nécessiter d'authentification."""

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


class CurrentUserView(generics.GenericAPIView):
    """Retourne le compte associé au jeton JWT fourni."""

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(self.get_serializer(request.user).data)


def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        database_status = "available"
        status_code = 200

    except Exception:
        database_status = "unavailable"
        status_code = 503

    return JsonResponse(
        {
            "status": "ok" if status_code == 200 else "error",
            "service": "deus-backend",
            "database": database_status,
        },
        status=status_code,
    )
