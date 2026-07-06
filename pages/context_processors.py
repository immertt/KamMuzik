from .models import SiteContent


def site_content(request):
    """SiteContent'i her template'e 'site' değişkeni olarak enjekte eder."""
    return {"site": SiteContent.load()}