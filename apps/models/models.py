from django.db import models
from apps.configuration.models import BaseModel
from apps.accounts.models import CustomUser
# Create your models here.


class Model(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=50)
    storage_location = models.CharField(max_length=500)  # File path or cloud location
    size = models.FloatField()  # In MB/GB
    

class ModelVariant(BaseModel):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="variants")
    variant_name = models.CharField(max_length=255)
    recommended_hardware = models.TextField()
    

class InteractionLog(BaseModel):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    interaction_data = models.JSONField()  # Captures interaction details
    interacted_at = models.DateTimeField(auto_now_add=True)
