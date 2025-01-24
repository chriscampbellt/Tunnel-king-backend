from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import OpenApiParameter, extend_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .schema import (LOGIN_RESPONSE_SCHEMA, PROFILE_DETAIL_SCHEMA,
                     PROFILE_PATCH_SCHEMA, PROFILE_PUT_SCHEMA,
                     USER_CREATE_RESPONSE_SCHEMA)
from .serializers import (AuthTokenSerializer, CreateUserSerializer,
                          ForgotPasswordSerializer, ResetPasswordSerializer,
                          SetPasswordSerializer, UserProfileSerializer)

User = get_user_model()


@extend_schema(responses=LOGIN_RESPONSE_SCHEMA)
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, request, format=None) -> Response:
        serializer = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @extend_schema(responses=PROFILE_DETAIL_SCHEMA)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(responses=PROFILE_PATCH_SCHEMA)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(responses=PROFILE_PUT_SCHEMA)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


@extend_schema(responses=USER_CREATE_RESPONSE_SCHEMA)
class SignUpAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Set a new password",
    description="API endpoint to set a new password for a user using a valid UID and token.",
    parameters=[],
    request=SetPasswordSerializer,
    responses={
        200: OpenApiParameter(
            name="detail", description="Password has been set successfully.", type=str
        ),
        400: OpenApiParameter(
            name="detail",
            description="Invalid user, token, or serializer errors.",
            type=str,
        ),
    },
)
class SetPasswordAPIView(APIView):
    """
    API view to set a new password for a user based on a valid token and UID.
    """

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validate the token
        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and save the new password
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": "Password has been set successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Authentication"],
    summary="Get token to reset password",
    description="API endpoint to send a password reset email",
    parameters=[],
    request=ForgotPasswordSerializer,
    responses={
        200: OpenApiParameter(
            name="detail", description="Password has been set successfully.", type=str
        ),
        400: OpenApiParameter(
            name="detail",
            description="Invalid user, token, or serializer errors.",
            type=str,
        ),
    },
)
class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = get_object_or_404(User, email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            combined_token = f"{uid}:{token}"

            # TODO: Update the reset url according to frontend
            current_site = Site.objects.get_current()
            reset_url = f"http://{current_site.domain}/password-reset-confirm/?token={combined_token}/"

            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_url}",
                from_email="no-reply@example.com",
                recipient_list=[email],
            )

            return Response(
                {"detail": "Password reset email sent."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Authentication"],
    summary="Validate the token and reset the password",
    description="reset users password",
    parameters=[],
    request=ResetPasswordSerializer,
    responses={
        200: OpenApiParameter(
            name="detail", description="Password has been set successfully.", type=str
        ),
        400: OpenApiParameter(
            name="detail",
            description="Invalid user, token, or serializer errors.",
            type=str,
        ),
    },
)
class ResetPasswordAPIView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            new_password = serializer.validated_data["new_password"]
            user.set_password(new_password)
            user.save()

            return Response(
                {"detail": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
