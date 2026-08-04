from django.urls import path

from .views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    CurrentUserView,
    LogoutView,
    RegisterView,
    health_check,
)


urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", CookieTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/token/refresh/", CookieTokenRefreshView.as_view(), name="token-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", CurrentUserView.as_view(), name="current-user"),
]
