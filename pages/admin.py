from django.contrib import admin
from .models import SiteContent, StudioPhoto


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
            "fields": ["contact_email", "contact_phone"]
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
    list_display = ["__str__", "order", "is_visible"]
    list_editable = ["order", "is_visible"]
    list_filter = ["is_visible"]