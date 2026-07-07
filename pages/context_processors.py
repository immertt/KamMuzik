from .models import SiteContent


def site_content(request):
    """SiteContent'i her template'e 'site' değişkeni olarak enjekte eder."""
    return {"site": SiteContent.load()}

def admin_stats(request):
    """Admin dashboard için istatistikler. Sadece admin sayfalarında hesaplar."""
    if not request.path.startswith("/admin"):
        return {}

    from catalog.models import Song, VideoClip, Category
    from contact.models import ContactMessage
    from .models import StudioPhoto

    return {
        "stat_songs": Song.objects.count(),
        "stat_clips": VideoClip.objects.count(),
        "stat_categories": Category.objects.count(),
        "stat_studio_photos": StudioPhoto.objects.count(),
        "stat_messages_total": ContactMessage.objects.count(),
        "stat_messages_unread": ContactMessage.objects.filter(is_read=False).count(),
    }