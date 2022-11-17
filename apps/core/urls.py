from django.urls import path

from apps.core.views import js_reverse, js_upload_media

app_name = "core"

urlpatterns = [
    path("js-upload-media/", js_upload_media, name="js_upload_media"),
    path("js-reverse/", js_reverse, name="js_reverse"),
]
