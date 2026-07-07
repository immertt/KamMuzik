from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Song, VideoClip


class StaticViewSitemap(Sitemap):
    """Sabit sayfalar: anasayfa, katalog, iletişim."""
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["catalog:home", "catalog:catalog_list", "contact:contact"]

    def location(self, item):
        return reverse(item)


class SongSitemap(Sitemap):
    """Tüm yayında şarkılar."""
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return Song.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class VideoClipSitemap(Sitemap):
    """Tüm yayında klipler."""
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return VideoClip.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at