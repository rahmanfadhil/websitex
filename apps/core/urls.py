from django.urls import path

from apps.core.views import MediaCreateView

app_name = "core"

urlpatterns = [path("upload-media/", MediaCreateView.as_view(), name="media_create")]
