from django.urls import path

from apps.core.views import MediaCreateView, js_reverse

app_name = "core"

urlpatterns = [
    path("upload-media/", MediaCreateView.as_view(), name="media_create"),
    path("js-reverse/", js_reverse, name="js_reverse"),
]
