from rest_framework import serializers

from apps.ai_models.models import DownloadedModel


class DownloadedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadedModel
        fields = "__all__"
