from rest_framework import serializers
from .models import Album, Song
from django.db import transaction

class SongSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False) # Allow IDs to be passed for updates
    
    class Meta:
        model = Song
        fields = ['id', 'title', 'duration', 'track_number']

class AlbumSerializer(serializers.ModelSerializer):
    # This nests the songs inside the album response
    songs = SongSerializer(many=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'release_date', 'songs']
    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. Extract the nested songs data
        songs_data = validated_data.pop('songs', None)
        
        # 2. Update the Album fields (title, artist, etc.)
        instance.title = validated_data.get('title', instance.title)
        instance.artist = validated_data.get('artist', instance.artist)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.save()

        if songs_data is not None:
            # 3. Handle the nested Songs
            # Get IDs of songs already attached to this album
            existing_songs = {song.id: song for song in instance.songs.all()}
            new_song_ids = []

            for song_item in songs_data:
                song_id = song_item.get('id')
                if song_id and song_id in existing_songs:
                    # Update existing song
                    song = existing_songs[song_id]
                    song.title = song_item.get('title', song.title)
                    song.track_number = song_item.get('track_number', song.track_number)
                    song.duration = song_item.get('duration', song.duration)
                    song.save()
                    new_song_ids.append(song.id)
                else:
                    # Create new song
                    new_song = Song.objects.create(album=instance, **song_item)
                    new_song_ids.append(new_song.id)

            # Delete songs that were NOT in the request
            for song_id, song_obj in existing_songs.items():
                if song_id not in new_song_ids:
                    song_obj.delete()

        return instance
    def create(self, validated_data):
        # 1. Pop the nested 'songs' data out of the validated_data dictionary
        songs_data = validated_data.pop('songs')
        
        # 2. Create the Album instance first
        album = Album.objects.create(**validated_data)
        
        # 3. Create each Song instance, linking it to the new Album
        for song_data in songs_data:
            Song.objects.create(album=album, **song_data)
            
        return album