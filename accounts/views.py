from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()


class UserRegisterView(APIView):
    """
    API endpoint for registering a new user.
    Standardized response format is used for both success and error.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Save user
            user = serializer.save()

            # Success response
            return Response({
                "success": True,
                "message": "🎉 User registered successfully!",
                "data": UserSerializer(user).data   # return clean user data
            }, status=status.HTTP_201_CREATED)

        # Error response
        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving the logged-in user's profile.
    GET /api/accounts/profile/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Always return the currently logged-in user
        return self.request.user


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view that stores access + refresh tokens in HttpOnly cookies.
    """
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = serializer.validated_data
        access = tokens["access"]
        refresh = tokens["refresh"]

        response = Response({"success": True}, status=status.HTTP_200_OK)

        # ⚡ Store tokens in HttpOnly cookies
        response.set_cookie(
            key="access",
            value=str(access),
            httponly=settings.COOKIE_OPTIONS["httponly"],
            secure=settings.COOKIE_OPTIONS["secure"],
            samesite=settings.COOKIE_OPTIONS["samesite"],
            max_age=60 * 15,  # 15 minutes
            # max_age=10,  # 10 seconds to test on localhost
            domain=None
        )
        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=settings.COOKIE_OPTIONS["httponly"],
            secure=settings.COOKIE_OPTIONS["secure"],
            samesite=settings.COOKIE_OPTIONS["samesite"],
            max_age=60 * 60 * 24 * 7,  # 7 days (refresh)
            # max_age=20,  # 20 seconds to test on localhost
            domain=None
        )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token is None:
            return Response({"message": "Refresh token missing"}, status=status.HTTP_401_UNAUTHORIZED)


class CookieTokenRefreshView(TokenRefreshView):
    """
    Custom refresh view that:
    - Reads refresh token from cookie
    - Rotates refresh tokens (new refresh + blacklist old)
    - Sends both access & refresh back in cookies
    """
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        # pull refresh token from cookie
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token is None:
            return Response({"message": "Refresh token missing"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response({"message": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        # serializer.validated_data now contains access + maybe refresh
        data = serializer.validated_data
        access_token = data.get("access")
        # only if ROTATE_REFRESH_TOKENS = True
        new_refresh = data.get("refresh")

        response = Response({"access": access_token},
                            status=status.HTTP_200_OK)

        # set new access token cookie
        response.set_cookie(
            key="access",
            value=access_token,
            httponly=settings.COOKIE_OPTIONS["httponly"],
            secure=settings.COOKIE_OPTIONS["secure"],
            samesite=settings.COOKIE_OPTIONS["samesite"],
            max_age=60 * 15,  # 15 minutes
            # max_age=10,  # 10 seconds to test on localhost
            domain=None
        )

        # if rotation is enabled, set new refresh cookie too
        if new_refresh:
            response.set_cookie(
                key="refresh",
                value=new_refresh,
                httponly=settings.COOKIE_OPTIONS["httponly"],
                secure=settings.COOKIE_OPTIONS["secure"],
                samesite=settings.COOKIE_OPTIONS["samesite"],
                max_age=60 * 60 * 24 * 7,  # 7 days (refresh)
                # max_age=20,  # 20 seconds to test on localhost
                domain=None
            )

        return response


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        response = Response({"success": True}, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
