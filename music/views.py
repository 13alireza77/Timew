from django.views import generic
from .models import Album, song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse


class IndexView(generic.ListView):
    template_name = 'music/index.html'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'gener', 'album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'gener', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


def favorite(request, song_id):
    so = get_object_or_404(song, pk=song_id)
    try:
        if so.is_favorite:
            so.is_favorite = False
        else:
            so.is_favorite = True
        so.save()
    except (KeyError, so.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
