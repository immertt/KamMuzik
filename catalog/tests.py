from django.test import TestCase
from django.urls import reverse
from .models import Category, Tag, Song, VideoClip


class SlugGenerationTest(TestCase):
    """save() metodundaki otomatik slug üretimini test eder."""

    def test_song_slug_auto_generated(self):
        song = Song.objects.create(title="Eminem Rap God")
        self.assertEqual(song.slug, "eminem-rap-god")

    def test_slug_not_overwritten_if_provided(self):
        song = Song.objects.create(title="Test", slug="ozel-slug")
        self.assertEqual(song.slug, "ozel-slug")

    def test_category_slug_auto_generated(self):
        cat = Category.objects.create(name="Pop Müzik")
        self.assertEqual(cat.slug, "pop-muzik")


class TypeLabelTest(TestCase):
    """get_type_label() polimorfizmini test eder."""

    def test_song_label(self):
        song = Song.objects.create(title="Şarkı 1")
        self.assertEqual(song.get_type_label(), "Şarkı")

    def test_clip_label(self):
        clip = VideoClip.objects.create(title="Klip 1")
        self.assertEqual(clip.get_type_label(), "Klip")


class AbsoluteUrlTest(TestCase):
    """get_absolute_url() her model için doğru adresi döndürmeli."""

    def test_song_url(self):
        song = Song.objects.create(title="Şarkı X")
        expected = reverse("catalog:song_detail", kwargs={"slug": song.slug})
        self.assertEqual(song.get_absolute_url(), expected)

    def test_clip_url(self):
        clip = VideoClip.objects.create(title="Klip X")
        expected = reverse("catalog:clip_detail", kwargs={"slug": clip.slug})
        self.assertEqual(clip.get_absolute_url(), expected)


class EmbedIdTest(TestCase):
    """embed_id property'si farklı YouTube link formatlarını çözmeli."""

    def test_standard_watch_url(self):
        clip = VideoClip.objects.create(
            title="K1", youtube_url="https://www.youtube.com/watch?v=GR6r-jIryH0"
        )
        self.assertEqual(clip.embed_id, "GR6r-jIryH0")

    def test_url_with_playlist_params(self):
        clip = VideoClip.objects.create(
            title="K2",
            youtube_url="https://www.youtube.com/watch?v=GR6r-jIryH0&list=RDGR6r-jIryH0&start_radio=1",
        )
        self.assertEqual(clip.embed_id, "GR6r-jIryH0")

    def test_short_youtu_be_url(self):
        clip = VideoClip.objects.create(
            title="K3", youtube_url="https://youtu.be/GR6r-jIryH0"
        )
        self.assertEqual(clip.embed_id, "GR6r-jIryH0")

    def test_empty_url_returns_empty(self):
        clip = VideoClip.objects.create(title="K4")
        self.assertEqual(clip.embed_id, "")

from django.test import Client


class ViewStatusTest(TestCase):
    """Sayfaların doğru şekilde yüklendiğini (HTTP 200/404) test eder."""

    def setUp(self):
        self.client = Client()
        self.song = Song.objects.create(title="Yayında Şarkı", is_published=True)

    def test_home_page_loads(self):
        response = self.client.get(reverse("catalog:home"))
        self.assertEqual(response.status_code, 200)

    def test_catalog_page_loads(self):
        response = self.client.get(reverse("catalog:catalog_list"))
        self.assertEqual(response.status_code, 200)

    def test_song_detail_loads(self):
        response = self.client.get(self.song.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yayında Şarkı")

    def test_nonexistent_slug_returns_404(self):
        response = self.client.get(
            reverse("catalog:song_detail", kwargs={"slug": "olmayan-sarki"})
        )
        self.assertEqual(response.status_code, 404)


class PublishRuleTest(TestCase):
    """İş kuralı: yayında olmayan çalışmalar sitede görünmemeli."""

    def setUp(self):
        self.client = Client()
        self.published = Song.objects.create(title="Görünür Şarkı", is_published=True)
        self.draft = Song.objects.create(title="Taslak Şarkı", is_published=False)

    def test_draft_not_in_catalog(self):
        response = self.client.get(reverse("catalog:catalog_list"))
        self.assertContains(response, "Görünür Şarkı")
        self.assertNotContains(response, "Taslak Şarkı")

    def test_draft_detail_returns_404(self):
        # Yayında olmayan bir şarkının detay sayfasına doğrudan erişilememeli
        response = self.client.get(self.draft.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_published_detail_accessible(self):
        response = self.client.get(self.published.get_absolute_url())
        self.assertEqual(response.status_code, 200)