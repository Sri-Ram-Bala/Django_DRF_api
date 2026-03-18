from rest_framework import serializers
from .models import Album, Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'duration', 'track_number']

class AlbumSerializer(serializers.ModelSerializer):
    # This nests the songs inside the album response
    songs = SongSerializer(many=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'release_date', 'songs']
    
    def create(self, validated_data):
        # 1. Pop the nested 'songs' data out of the validated_data dictionary
        songs_data = validated_data.pop('songs')
        
        # 2. Create the Album instance first
        album = Album.objects.create(**validated_data)
        
        # 3. Create each Song instance, linking it to the new Album
        for song_data in songs_data:
            Song.objects.create(album=album, **song_data)
            
        return album