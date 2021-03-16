from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.pages.urls", namespace="pages")),
    path("", include("apps.users.urls", namespace="users")),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.views.defaults import page_not_found

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("404/", page_not_found, {"exception": Exception()}),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
