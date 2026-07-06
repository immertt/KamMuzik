from django.test import TestCase
from .models import SiteContent, StudioPhoto


class SiteContentSingletonTest(TestCase):
    """SiteContent'in her zaman tek kayıt (singleton) kaldığını test eder."""

    def test_load_creates_default(self):
        # Hiç kayıt yokken load() varsayılanlarla bir tane oluşturmalı
        self.assertEqual(SiteContent.objects.count(), 0)
        content = SiteContent.load()
        self.assertEqual(SiteContent.objects.count(), 1)
        self.assertTrue(content.about_title)  # varsayılan metin dolu gelmeli

    def test_always_single_row(self):
        # Birden fazla kaydetmeye çalışsak bile tek satır kalmalı
        SiteContent.load()
        second = SiteContent(about_title="İkinci")
        second.save()
        self.assertEqual(SiteContent.objects.count(), 1)

    def test_pk_always_one(self):
        content = SiteContent.load()
        self.assertEqual(content.pk, 1)

    def test_load_returns_existing(self):
        # İkinci load() yeni oluşturmamalı, mevcut olanı getirmeli
        first = SiteContent.load()
        first.about_title = "Değiştirilmiş"
        first.save()
        second = SiteContent.load()
        self.assertEqual(second.about_title, "Değiştirilmiş")


class StudioPhotoTest(TestCase):
    """StudioPhoto sıralama ve görünürlük davranışı."""

    def test_ordering_by_order_field(self):
        # order alanına göre sıralanmalı
        p3 = StudioPhoto.objects.create(caption="C", order=3)
        p1 = StudioPhoto.objects.create(caption="A", order=1)
        p2 = StudioPhoto.objects.create(caption="B", order=2)
        photos = list(StudioPhoto.objects.all())
        self.assertEqual(photos, [p1, p2, p3])

    def test_str_uses_caption(self):
        photo = StudioPhoto.objects.create(caption="Kayıt Odası", order=1)
        self.assertEqual(str(photo), "Kayıt Odası")