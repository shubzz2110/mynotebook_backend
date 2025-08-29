from django.urls import path
from .views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutView,
    UserRegisterView,
    ProfileView
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),

    # JWT with cookies
    path("login/", CookieTokenObtainPairView.as_view(), name="cookie_login"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="cookie_token_refresh"),
    path("logout/", LogoutView.as_view(), name="cookie_logout"),
]
