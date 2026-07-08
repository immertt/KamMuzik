from django.contrib import admin
from .models import Category, Tag, Song, VideoClip
from django.utils.html import format_html
from django.db import models
from django.forms import CheckboxSelectMultiple

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["kapak_onizleme", "title", "category", "release_date", "is_published"]
    list_display_links = ["title"]
    list_editable = ["is_published"]
    list_filter = ["category"]
    search_fields = ["title", "description"]
    date_hierarchy = "release_date"
    prepopulated_fields = {"slug": ["title"]}
    list_per_page = 25
    ordering = ["-release_date", "-created_at"]
    readonly_fields = ["created_at", "updated_at", "kapak_form_onizleme"]
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    actions = ["yayinla", "yayindan_kaldir"]

    fieldsets = [
        ("Temel Bilgiler", {
            "fields": ["title", "slug", "description", "cover_image", "release_date"]
        }),
        ("Sınıflandırma", {
            "fields": ["category", "tags", "is_published"]
        }),
        ("Müzik Bağlantıları", {
            "fields": ["spotify_url", "apple_music_url", "youtube_url", "duration"],
            "description": "Platform linklerini tam adresleriyle yapıştırın (isteğe bağlı).",
        }),
        ("Kayıt Bilgisi", {
            "fields": ["created_at", "updated_at"],
            "classes": ["collapse"],
        }),
    ]

    def kapak_onizleme(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width:46px;height:46px;object-fit:cover;border-radius:6px;" />',
                obj.cover_image.url
            )
        return format_html('<span style="opacity:0.4;">—</span>')
    kapak_onizleme.short_description = "Kapak"

    def kapak_form_onizleme(self, obj):
        if obj and obj.cover_image:
            return format_html(
                '<img src="{}" style="max-width:220px;border-radius:10px;'
                'box-shadow:0 4px 18px rgba(0,0,0,0.4);" />',
                obj.cover_image.url
            )
        return format_html('<span style="opacity:0.5;">Henüz kapak yüklenmedi.</span>')
    kapak_form_onizleme.short_description = "Mevcut Kapak"

    @admin.action(description="Seçili şarkıları yayınla")
    def yayinla(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} şarkı yayınlandı.")

    @admin.action(description="Seçili şarkıları yayından kaldır")
    def yayindan_kaldir(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} şarkı yayından kaldırıldı.")


@admin.register(VideoClip)
class VideoClipAdmin(admin.ModelAdmin):

    def kapak_onizleme(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width:46px;height:46px;object-fit:cover;border-radius:6px;" />',
                obj.cover_image.url
            )
        return format_html('<span style="opacity:0.4;">—</span>')
    kapak_onizleme.short_description = "Kapak"

    list_display = ["kapak_onizleme", "title", "category", "director", "release_date", "is_published"]
    list_filter = ["is_published", "category", "tags"]
    search_fields = ["title", "description", "director"]
    filter_horizontal = ["tags"]
    date_hierarchy = "release_date"
    prepopulated_fields = {"slug": ["title"]}

    fieldsets = [
        ("Temel Bilgiler", {
            "fields": ["title", "slug", "description", "cover_image", "kapak_form_onizleme", "release_date"]
        }),
        ("Sınıflandırma", {
            "fields": ["category", "tags", "is_published"]
        }),
        ("Klip Bilgileri", {
            "fields": ["youtube_url", "director"]
        }),
    ]

admin.site.site_header = "Kam Müzik Yönetim Paneli"
admin.site.site_title = "Kam Müzik"
admin.site.index_title = "İçerik Yönetimi"