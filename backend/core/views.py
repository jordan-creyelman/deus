from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer


def set_auth_cookie(response, name, value, max_age):
    response.set_cookie(
        name,
        value,
        max_age=max_age,
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        path="/",
    )


class CookieTokenObtainPairView(TokenObtainPairView):
    """Connecte l'utilisateur et place les JWT dans des cookies HttpOnly."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            set_auth_cookie(response, settings.JWT_ACCESS_COOKIE, response.data["access"], 900)
            set_auth_cookie(
                response,
                settings.JWT_REFRESH_COOKIE,
                response.data["refresh"],
                604800,
            )
            response.data = {"detail": "Connexion réussie."}

        return response


class CookieTokenRefreshView(generics.GenericAPIView):
    """Renouvelle les cookies JWT à partir du refresh token HttpOnly."""

    serializer_class = TokenRefreshSerializer
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        refresh = request.COOKIES.get(settings.JWT_REFRESH_COOKIE)
        if not refresh:
            return Response(
                {"detail": "Jeton de renouvellement absent."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(data={"refresh": refresh})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response(
                {"detail": "Jeton de renouvellement invalide."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        tokens = serializer.validated_data

        response = Response({"detail": "Session renouvelée."})
        set_auth_cookie(response, settings.JWT_ACCESS_COOKIE, tokens["access"], 900)
        if "refresh" in tokens:
            set_auth_cookie(
                response,
                settings.JWT_REFRESH_COOKIE,
                tokens["refresh"],
                604800,
            )
        return response


class LogoutView(generics.GenericAPIView):
    """Invalide le refresh token et supprime les cookies de session."""

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        refresh = request.COOKIES.get(settings.JWT_REFRESH_COOKIE)
        if refresh:
            try:
                RefreshToken(refresh).blacklist()
            except TokenError:
                pass

        response = Response({"detail": "Déconnexion réussie."})
        response.delete_cookie(settings.JWT_ACCESS_COOKIE, path="/")
        response.delete_cookie(settings.JWT_REFRESH_COOKIE, path="/")
        return response


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
