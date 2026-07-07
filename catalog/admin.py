from django.contrib import admin
from .models import Category, Tag, Song, VideoClip
from django.utils.html import format_html


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

    def kapak_onizleme(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width:46px;height:46px;object-fit:cover;border-radius:6px;" />',
                obj.cover_image.url
            )
        return format_html('<span style="opacity:0.4;">—</span>')
    kapak_onizleme.short_description = "Kapak"

    list_display = ["kapak_onizleme", "title", "category", "release_date", "is_published"]
    list_filter = ["is_published", "category", "tags"]
    search_fields = ["title", "description"]
    filter_horizontal = ["tags"]
    date_hierarchy = "release_date"
    prepopulated_fields = {"slug": ["title"]}

    fieldsets = [
        ("Temel Bilgiler", {
            "fields": ["title", "slug", "description", "cover_image", "release_date"]
        }),
        ("Sınıflandırma", {
            "fields": ["category", "tags", "is_published"]
        }),
        ("Müzik Bağlantıları", {
            "fields": ["spotify_url", "apple_music_url", "youtube_url", "duration"]
        }),
    ]


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
            "fields": ["title", "slug", "description", "cover_image", "release_date"]
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