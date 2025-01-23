from django.contrib import admin

from .models import DownloadedModel, OllamaModel


@admin.register(OllamaModel)
class OllamaModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "status",
        "activate_date",
        "deactivate_date",
        "name",
        "description",
    )
    list_filter = ("created", "modified", "activate_date", "deactivate_date")
    search_fields = ("name",)


@admin.register(DownloadedModel)
class DownloadedModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "status",
        "activate_date",
        "deactivate_date",
        "model",
        "organization",
        "model_status",
    )
    list_filter = (
        "created",
        "modified",
        "activate_date",
        "deactivate_date",
        "model",
        "organization",
    )
