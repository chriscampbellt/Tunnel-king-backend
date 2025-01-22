from django.db import models

from apps.configuration.models import BaseModel


# Create your models here.
class ServerInstance(BaseModel):
    model = models.ForeignKey("models.Model", on_delete=models.CASCADE)
    container_id = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=[
            ("active", "Active"),
            ("standby", "Standby"),
            ("terminated", "Terminated"),
        ],
    )


class ScalingPolicy(BaseModel):
    model = models.ForeignKey("models.Model", on_delete=models.CASCADE)
    max_instances = models.PositiveIntegerField(default=1)
    scale_down_time = models.PositiveIntegerField(
        help_text="Minutes of inactivity before scaling down."
    )
