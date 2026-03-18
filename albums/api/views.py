
# Create your views here.
from rest_framework import viewsets
from .models import Album, Song
from .serializers import AlbumSerializer, SongSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class SongViewSet(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    def get_queryset(self):
        # We access the 'album_pk' from the URL keywords
        if 'album_pk' in self.kwargs:
            # Relational access
            return Song.objects.filter(album_id=self.kwargs['album_pk'])
        # Selective (flat) access
        return Song.objects.all()
    def perform_create(self, serializer):
        # Automatically set the album_id from the URL prefix
        serializer.save(album_id=self.kwargs['album_pk'])