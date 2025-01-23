from django.db import models
from django_extensions.db.models import ActivatorModel, TimeStampedModel

from .choices import LargeLanguageModelStatusChoices


class OllamaModel(TimeStampedModel, ActivatorModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Name of the model (e.g., llama2, mistral).",
    )
    description = models.TextField(
        blank=True, null=True, help_text="Brief description of the model."
    )

    def __str__(self):
        return self.name


class DownloadedModel(TimeStampedModel, ActivatorModel):
    model = models.ForeignKey(
        OllamaModel,
        on_delete=models.CASCADE,
        related_name="downloads",
        help_text="The model that was downloaded.",
    )
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="downloaded_models",
    )
    model_status = models.CharField(
        choices=LargeLanguageModelStatusChoices,
        default=LargeLanguageModelStatusChoices.DOWNLOADING,
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("model", "organization")
