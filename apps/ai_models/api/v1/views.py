from rest_framework import generics

from apps.ai_models.api.v1.serializers import DownloadedModelSerializer
from apps.ai_models.models import DownloadedModel


class DownloadModelAPIView(generics.ListCreateAPIView):
    serializer_class = DownloadedModelSerializer
    queryset = DownloadedModel.objects.all()
