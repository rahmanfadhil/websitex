from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import finders
from django.http.response import FileResponse
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.views.i18n import JavaScriptCatalog


# Serve the service worker code in root
def service_worker(request):
    path = finders.find("dist/sw.js")
    return FileResponse(open(path, "rb"), content_type="application/javascript")


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("blog/", include(wagtail_urls)),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.core.urls", namespace="core")),
    path("", include("apps.pages.urls", namespace="pages")),
    path("", include("apps.users.urls", namespace="users")),
    path("service-worker.js", service_worker, name="service_worker"),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.views.defaults import page_not_found

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("404/", page_not_found, {"exception": Exception()}),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
