from django.urls import path

from apps.ai_models.api.v1.views import DownloadModelAPIView

urlpatterns = [
    path("download/", DownloadModelAPIView.as_view(), name="download"),
]
