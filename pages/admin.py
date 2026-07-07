from django.contrib import admin
from .models import SiteContent, StudioPhoto
from django.utils.html import format_html


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Hakkımızda Bölümü", {
            "fields": ["about_title", "about_text"]
        }),
        ("Stüdyo Bölümü", {
            "fields": ["studio_title", "studio_text"]
        }),
        ("İletişim Bilgileri", {
            "fields": ["contact_email", "contact_phone", "map_embed_url"]
        }),
        ("Panel Ayarları", {
            "fields": ["hero_image", "show_recent_actions"]
        }),
    ]

    def has_add_permission(self, request):
        # Singleton: zaten bir kayıt varsa "ekle" butonunu gizle
        return not SiteContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Tek içerik kaydı silinemesin
        return False


@admin.register(StudioPhoto)
class StudioPhotoAdmin(admin.ModelAdmin):
    list_display = ["onizleme", "__str__", "order", "is_visible"]
    list_editable = ["order", "is_visible"]
    list_filter = ["is_visible"]

    def onizleme(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px;height:45px;object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return format_html('<span style="opacity:0.4;">—</span>')
    onizleme.short_description = "Önizleme"