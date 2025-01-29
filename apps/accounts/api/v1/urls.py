from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (ForgotPasswordAPIView, LogoutView, ResetPasswordAPIView,
                    SetPasswordAPIView, SignUpAPIView, UserLoginAPIView,
                    UserProfileView)

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="create"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "set-password/<uidb64>/<token>/",
        SetPasswordAPIView.as_view(),
        name="set_admin_password",
    ),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset_password"),
]
