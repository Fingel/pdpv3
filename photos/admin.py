from django.contrib import admin
from django.utils.safestring import mark_safe

from photos.models import PdpImage


class PdpImageAdmin(admin.ModelAdmin):
    list_display = ["id", "full_url", "date", "description", "private", "preview"]
    search_fields = ["description"]
    readonly_fields = ["thumb", "preview", "full_url"]
    fields = [
        "image",
        "description",
        "private",
        "hidden",
        "thumb",
        "preview",
        "full_url",
    ]

    def preview(self, obj):
        return mark_safe(
            f'<a href="{obj.image.url}"><img height="150" src="{obj.thumb.url}"></a>'
        )

    def full_url(self, obj):
        return obj.image.url


admin.site.register(PdpImage, PdpImageAdmin)
