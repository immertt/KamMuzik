from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("katalog/", views.catalog_list, name="catalog_list"),
    path("sarki/<slug:slug>/", views.song_detail, name="song_detail"),
    path("klip/<slug:slug>/", views.clip_detail, name="clip_detail"),
]