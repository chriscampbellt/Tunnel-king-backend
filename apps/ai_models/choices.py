from django.db import models


class LargeLanguageModelStatusChoices(models.TextChoices):
    RUNNING = "RUNNING", "Running"
    DOWNLOADED = "DOWNLOADED", "Downloaded"
    DOWNLOADING = "DOWNLOADING", "Downloading"
    STOPPED = "STOPPED", "Stopped"
    DOWNLOADING_FAILED = "DOWNLOADING_FAILED", "Downloading Failed"
