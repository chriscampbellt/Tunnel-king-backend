from django.db import models
from apps.accounts.models import CustomUser

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Configuration(BaseModel):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    data = models.JSONField()  # Stores configuration settings


class ModelServer(BaseModel):
    name = models.CharField(max_length=255)
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[("running", "Running"), ("stopped", "Stopped"), ("error", "Error")],
    )
    

class DeploymentLog(BaseModel):
    server = models.ForeignKey(ModelServer, on_delete=models.CASCADE)
    message = models.TextField()
    logged_at = models.DateTimeField(auto_now_add=True)
