from django.contrib import admin
from .models import SiteContent, StudioPhoto
from django.utils.html import format_html


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    readonly_fields = ["hero_onizleme"]

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
            "fields": ["hero_image", "hero_onizleme", "show_recent_actions"]
        }),
    ]

    def has_add_permission(self, request):
        # Singleton: zaten bir kayıt varsa "ekle" butonunu gizle
        return not SiteContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Tek içerik kaydı silinemesin
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Singleton: liste yerine doğrudan tek kaydın düzenleme sayfasına git
        from django.shortcuts import redirect
        obj = SiteContent.load()
        return redirect("admin:pages_sitecontent_change", obj.pk)

    def hero_onizleme(self, obj):
        if obj and obj.hero_image:
            return format_html(
                '<img src="{}" style="max-width:320px;border-radius:10px;'
                'box-shadow:0 4px 18px rgba(0,0,0,0.4);" />',
                obj.hero_image.url
            )
        return format_html('<span style="opacity:0.5;">Henüz hero görseli yüklenmedi.</span>')
    hero_onizleme.short_description = "Mevcut Hero Görseli"

@admin.register(StudioPhoto)
class StudioPhotoAdmin(admin.ModelAdmin):
    list_display = ["onizleme", "caption", "order", "is_visible"]
    list_display_links = ["onizleme"]
    list_editable = ["order", "is_visible"]
    list_filter = ["is_visible"]
    ordering = ["order", "id"]
    readonly_fields = ["form_onizleme"]

    fieldsets = [
        ("Fotoğraf", {
            "fields": ["image", "form_onizleme", "caption"]
        }),
        ("Görünüm Ayarları", {
            "fields": ["order", "is_visible"],
            "description": "Sıra numarası küçük olan fotoğraf galeride önce görünür. Görünmez yapılan fotoğraflar sitede gösterilmez.",
        }),
    ]

    def onizleme(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px;height:45px;object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return format_html('<span style="opacity:0.4;">—</span>')
    onizleme.short_description = "Önizleme"

    def form_onizleme(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-width:280px;border-radius:10px;'
                'box-shadow:0 4px 18px rgba(0,0,0,0.4);" />',
                obj.image.url
            )
        return format_html('<span style="opacity:0.5;">Henüz fotoğraf yüklenmedi.</span>')
    form_onizleme.short_description = "Mevcut Fotoğraf"