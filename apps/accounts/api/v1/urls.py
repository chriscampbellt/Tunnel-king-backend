from django.urls import path
from knox import views as knox_views

from .views import (ForgotPasswordAPIView, LoginView, ResetPasswordAPIView,
                    SetPasswordAPIView, SignUpAPIView, UserProfileView)

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="create"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="knox_login"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    path(
        "set-password/<uidb64>/<token>/",
        SetPasswordAPIView.as_view(),
        name="set_admin_password",
    ),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset_password"),
]
