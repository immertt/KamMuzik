from django.db import models


class SiteContent(models.Model):
    """Sitedeki sabit metin içerikleri (tek satır — singleton).
    Admin panelden düzenlenir; başlangıçta varsayılan değerlerle gelir."""

    about_title = models.CharField(
        "Hakkımızda başlığı",
        max_length=200,
        default="Müziğin Kalbinde Üretim",
    )
    about_text = models.TextField(
        "Hakkımızda metni",
        default=(
            "Kam Müzik olarak, uluslararası standartlarda ses kayıt, "
            "albüm ve klip yapımı hizmetleri sunuyoruz. Sanatçılarımızın "
            "eserlerini dijital platformlarda dinleyicilerle buluşturuyoruz."
        ),
    )
    studio_title = models.CharField(
        "Stüdyo başlığı",
        max_length=200,
        default="Stüdyomuz",
    )
    studio_text = models.TextField(
        "Stüdyo açıklaması",
        blank=True,
        default="Son teknoloji ekipmanlarla donatılmış profesyonel kayıt stüdyomuz.",
    )
    contact_email = models.EmailField("İletişim e-postası", default="info@kammuzik.com")
    contact_phone = models.CharField("Telefon", max_length=40, default="+90 555 123 45 67")

    class Meta:
        verbose_name = "Site İçeriği"
        verbose_name_plural = "Site İçeriği"

    def __str__(self):
        return "Site İçeriği"

    def save(self, *args, **kwargs):
        """Singleton: her zaman pk=1 olur, ikinci kayıt oluşturulamaz."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """İçeriği getir; yoksa varsayılanlarla oluştur."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class StudioPhoto(models.Model):
    """Stüdyo galerisi fotoğrafları — admin istediği kadar ekler/sıralar."""

    image = models.ImageField("Fotoğraf", upload_to="studio/")
    caption = models.CharField("Açıklama", max_length=200, blank=True)
    order = models.PositiveIntegerField("Sıra", default=0)
    is_visible = models.BooleanField("Görünür mü?", default=True)

    class Meta:
        verbose_name = "Stüdyo Fotoğrafı"
        verbose_name_plural = "Stüdyo Fotoğrafları"
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Stüdyo fotoğrafı #{self.pk}"