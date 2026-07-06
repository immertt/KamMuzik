from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
            verbose_name = "Kategori"
            verbose_name_plural = "Kategoriler"
            ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Production(models.Model):
    title = models.CharField("Başlık", max_length=200)
    slug = models.SlugField("Kısa ad (URL)", max_length=220, unique=True, blank=True)
    description = models.TextField("Açıklama", blank=True)
    cover_image = models.ImageField("Kapak görseli", upload_to="covers/", blank=True, null=True)
    release_date = models.DateField("Yayın tarihi", blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)ss",
        verbose_name="Kategori",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="%(class)ss", verbose_name="Etiketler")
    is_published = models.BooleanField("Yayında mı?", default=True)
    created_at = models.DateTimeField("Oluşturulma", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme", auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-release_date", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Song(Production):
    spotify_url = models.URLField("Spotify linki", blank=True)
    apple_music_url = models.URLField("Apple Music linki", blank=True)
    youtube_url = models.URLField("YouTube linki", blank=True)
    duration = models.DurationField("Süre", blank=True, null=True)

    class Meta(Production.Meta):
        verbose_name = "Şarkı"
        verbose_name_plural = "Şarkılar"


class VideoClip(Production):
    youtube_url = models.URLField("YouTube linki", blank=True)
    director = models.CharField("Yönetmen", max_length=200, blank=True)

    class Meta(Production.Meta):
        verbose_name = "Video Klip"
        verbose_name_plural = "Video Klipler"