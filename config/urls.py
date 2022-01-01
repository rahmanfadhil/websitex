from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("blog/", include(wagtail_urls)),
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls", namespace="core")),
    path("", include("apps.pages.urls", namespace="pages")),
    path("", include("apps.users.urls", namespace="users")),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.views.defaults import page_not_found

    # Serve user-uploaded content
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Enable Django Debug Toolbar and show 404 page
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("404/", page_not_found, {"exception": Exception()}),
    ]
