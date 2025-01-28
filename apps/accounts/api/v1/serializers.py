from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework_simplejwt.serializers import \
    TokenObtainPairSerializer as RestSimpleJwtTokenObtainPairSerializer

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=5)
    password2 = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, data: dict) -> dict:
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data: dict) -> User:
        validated_data.pop("password2")
        return super().create(validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)
        user: User = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class LoginResponseSerializer(serializers.Serializer):
    expiry = serializers.DateTimeField()
    token = serializers.CharField()
    user = UserProfileSerializer()

    def get_user(self, obj):
        user = obj.get("user")
        return {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        combined_token = data.get("token")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        try:
            uid, token = combined_token.split(":")
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (ValueError, TypeError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(
                {"combined_token": "Invalid or malformed token."}
            )

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {"combined_token": "Invalid or expired token."}
            )

        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "date_joined"]


class UserLoginSerializer(RestSimpleJwtTokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        data["user"] = UserSerializer(self.user).data

        return data
