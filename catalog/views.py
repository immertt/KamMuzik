from django.shortcuts import render, get_object_or_404
from itertools import chain
from .models import Song, VideoClip, Category, Tag
from pages.models import SiteContent, StudioPhoto
from django.core.paginator import Paginator


def home(request):
    songs = Song.objects.filter(is_published=True)[:6]
    clips = VideoClip.objects.filter(is_published=True)[:6]
    context = {
        "songs": songs,
        "clips": clips,
        "content": SiteContent.load(),
        "studio_photos": StudioPhoto.objects.filter(is_visible=True),
    }
    return render(request, "catalog/home.html", context)


def catalog_list(request):
    songs = Song.objects.filter(is_published=True)
    clips = VideoClip.objects.filter(is_published=True)
    all_productions = sorted(
        chain(songs, clips),
        key=lambda p: p.release_date or p.created_at.date(),
        reverse=True,
    )

    # Sayfalama: her sayfada 12 çalışma
    paginator = Paginator(all_productions, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "productions": page_obj,       # şablon bunun üzerinden döner
        "page_obj": page_obj,          # sayfalama kontrolleri için
        "categories": Category.objects.all(),
    }
    return render(request, "catalog/catalog_list.html", context)

def song_detail(request, slug):
    song = get_object_or_404(Song, slug=slug, is_published=True)
    return render(request, "catalog/song_detail.html", {"song": song})


def clip_detail(request, slug):
    clip = get_object_or_404(VideoClip, slug=slug, is_published=True)
    return render(request, "catalog/clip_detail.html", {"clip": clip})