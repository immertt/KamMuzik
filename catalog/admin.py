from django.contrib import admin
from .models import Category, Tag, Song, VideoClip


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
    list_display = ["title", "category", "release_date", "is_published"]
    list_filter = ["is_published", "category", "tags"]
    search_fields = ["title", "description"]
    filter_horizontal = ["tags"]
    date_hierarchy = "release_date"


@admin.register(VideoClip)
class VideoClipAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "director", "release_date", "is_published"]
    list_filter = ["is_published", "category", "tags"]
    search_fields = ["title", "description", "director"]
    filter_horizontal = ["tags"]
    date_hierarchy = "release_date"