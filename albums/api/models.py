from django.db import models

# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    release_date = models.DateField()

    def __str__(self):
        return self.title

class Song(models.Model):
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    track_number = models.PositiveIntegerField()

    def __str__(self):
        return self.title