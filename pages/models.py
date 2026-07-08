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

    map_embed_url = models.URLField(
        "Google Harita linki (embed src)",
        max_length=1000,
        blank=True,
        help_text="Google Haritalar → Paylaş → Harita yerleştir → iframe içindeki src=\"...\" linkini yapıştır.",
    )
    hero_image = models.ImageField(
        "Hero arka plan görseli",
        upload_to="hero/",
        blank=True,
        null=True,
        help_text="Anasayfa üst bölümünün arka planı. Yatay, koyu tonlu bir stüdyo fotoğrafı ideal.",
    )

    hero_title = models.CharField(
        "Hero başlığı (1. satır)",
        max_length=200,
        default="Dünya Standartlarında",
    )
    hero_title_accent = models.CharField(
        "Hero başlığı (2. satır - vurgulu)",
        max_length=200,
        default="Ses ve Yapım",
    )
    hero_subtitle = models.CharField(
        "Hero alt açıklaması",
        max_length=300,
        default="Albüm & single yapımı, klip çekimi ve dijital platform yayıncılığı.",
    )

    show_recent_actions = models.BooleanField(
        "Panelde 'Son Eylemler'i göster",
        default=True,
        help_text="Kapatılırsa yönetim panosunda son işlemler listesi gizlenir.",
    )

    logo = models.ImageField(
        "Logo",
        upload_to="logo/",
        blank=True,
        null=True,
        help_text="Sitenin ve panelin her yerinde kullanılacak logo. Kare veya yatay, şeffaf arka planlı (PNG) ideal.",
    )

    THEME_CHOICES = [
        ("mavi", "Mavi (Varsayılan)"),
        ("yesil", "Yeşil"),
        ("mor", "Mor"),
        ("turuncu", "Turuncu"),
    ]
    theme = models.CharField(
        "Site Teması",
        max_length=20,
        choices=THEME_CHOICES,
        default="mavi",
        help_text="Sitenin genel renk temasını belirler.",
    )


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

    @property
    def whatsapp_number(self):
        """contact_phone'dan wa.me formatını üretir.
        Türkiye formatını uluslararası formata çevirir:
        - Rakam dışındaki her şeyi temizler (+, boşluk, tire, parantez)
        - Baştaki 0'ı atıp 90 ekler (05321112233 -> 905321112233)
        - Zaten 90 ile başlıyorsa dokunmaz
        """
        import re
        digits = re.sub(r"[^\d]", "", self.contact_phone or "")
        if digits.startswith("90"):
            return digits                    # zaten uluslararası: 905321112233
        if digits.startswith("0"):
            return "90" + digits[1:]         # 05321112233 -> 905321112233
        if digits.startswith("5"):
            return "90" + digits             # 5321112233 -> 905321112233
        return digits                         # bilinmeyen format: olduğu gibi

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