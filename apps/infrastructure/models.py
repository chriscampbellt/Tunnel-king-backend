from django.db import models

from apps.configuration.models import BaseModel


# Create your models here.
class Infrastructure(BaseModel):
    component_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("active", "Active"),
            ("down", "Down"),
            ("maintenance", "Maintenance"),
        ],
    )
    last_checked = models.DateTimeField(auto_now=True)


class Log(models.Model):
    message = models.TextField()
    component = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)
    logged_at = models.DateTimeField(auto_now_add=True)


class SecurityPolicy(BaseModel):
    name = models.CharField(max_length=255)
    rules = models.JSONField()  # e.g., password complexity, 2FA requirements
