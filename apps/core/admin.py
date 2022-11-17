from django.contrib import admin

from apps.core.models import Media


class MediaAdmin(admin.ModelAdmin):
    model = Media
    list_display = ("file", "author", "created_at")


admin.site.register(Media, MediaAdmin)
