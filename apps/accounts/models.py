from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .managers import UserManager


class User(AbstractUser):
    """
    CustomUser is a custom user model that extends Django's AbstractUser.
    It uses email as the unique identifier instead of the username.
    """

    username = None
    email = models.EmailField(_("email address"), unique=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="created_users",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


class Credential(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="credentials"
    )  # Link to User
    token = models.CharField(max_length=255, unique=True)  # API or session token
    expires_at = models.DateTimeField()  # Expiry time for the token

    def __str__(self):
        return f"Credential for {self.user.username}"
