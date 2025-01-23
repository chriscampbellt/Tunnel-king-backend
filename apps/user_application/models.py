from django.db import models

from apps.configuration.models import BaseModel

# Create your models here.
# class AccountCreation(BaseModel):
#     user = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE)


class ModelInteraction(BaseModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    model = models.ForeignKey("models.Model", on_delete=models.CASCADE)
    action = models.CharField(max_length=100)  # e.g., "run", "stop"
    timestamp = models.DateTimeField(auto_now_add=True)
