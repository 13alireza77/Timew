from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Permission


# Create your models here.

class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    gener = models.CharField(max_length=100)
    album_logo = models.ImageField(upload_to="gallery")
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + " - " + self.artist


class song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)
    audio_file = models.FileField(default='')

    def __str__(self):
        return self.song_title

    def get_absolute_url(self):
        return reverse('music:songs', kwargs={'filter_by': 'all'})
