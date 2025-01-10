from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    CustomUser is a custom user model that extends Django's AbstractUser.
    It uses email as the unique identifier instead of the username.
    """

    # The username field is set to None to disable it.
    username = None

    # The email field is set to be unique because it is the unique identifier.
    email = models.EmailField(_("email address"), unique=True)
    is_admin = models.BooleanField(default=False)  # True if the user is an admin
    department = models.CharField(max_length=100, null=True, blank=True)  # Department of the user
    job_title = models.CharField(max_length=100, null=True, blank=True)  # User's job title
    permission_level = models.CharField(max_length=50, default="User")  # Permission level (Admin/User/etc.)


    # Specifies the field to be used as the unique identifier for the user.
    USERNAME_FIELD = "email"

    # A list of fields that will be prompted for when creating a user
    # via the createsuperuser command. If empty, the USERNAME_FIELD is
    # the only required.
    REQUIRED_FIELDS = []

    # The CustomUserManager allows the creation of a user where email
    # is the unique identifier.
    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Define a Role model to represent various roles in the system
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Name of the role (e.g., Admin, Manager, Viewer)
    description = models.TextField(null=True, blank=True)  # Optional description for the role

    def __str__(self):
        return self.name


# Many-to-Many relationship between User and Role
class UserRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="roles")  # Link to User
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")  # Link to Role
    assigned_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the role was assigned

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


# For managing user credentials
class Credential(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="credentials")  # Link to User
    token = models.CharField(max_length=255, unique=True)  # API or session token
    expires_at = models.DateTimeField()  # Expiry time for the token

    def __str__(self):
        return f"Credential for {self.user.username}"    