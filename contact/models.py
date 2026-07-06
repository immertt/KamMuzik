from django.db import models


class ContactMessage(models.Model):
    """Ziyaretçilerin iletişim formundan gönderdiği mesajlar."""

    name = models.CharField("Ad Soyad", max_length=120)
    email = models.EmailField("E-posta")
    subject = models.CharField("Konu", max_length=200, blank=True)
    message = models.TextField("Mesaj")
    created_at = models.DateTimeField("Gönderim tarihi", auto_now_add=True)
    is_read = models.BooleanField("Okundu mu?", default=False)

    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject or 'Konusuz'}"