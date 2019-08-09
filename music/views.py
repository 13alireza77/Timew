from django.views import generic
from .models import Album, song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth import authenticate

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


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


class songCreate(CreateView):
    model = song
    fields = '__all__'


def song_delete(request, song_id, album_id):
    album = get_object_or_404(Album, pk=album_id)
    son = song.objects.filter(pk=song_id)
    son.delete()
    context = {
        'album': album
    }
    return render(request, 'music/detail.html', context)


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


def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for son in album.song_set.all():
                    song_ids.append(son.pk)
            user_songs = song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                user_songs = user_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            user_songs = []
        context = {
            'song_list': user_songs,
            'filter_by': filter_by
        }
        return render(request, 'music/songs.html', context)


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except Album.DoesNotExist:
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
