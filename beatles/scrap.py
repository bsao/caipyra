import json

import spotipy
from PyLyrics import PyLyrics

BEATLES_URN = 'spotify:artist:3WrFJ7ztbogyGnTHbHJFl2'

# connection to PyLyrics service
lyrics = PyLyrics()

# connection to Spotify public API
spotify = spotipy.Spotify()

# get artists information
artist = spotify.artist(BEATLES_URN)
artist_name = artist.get('name')

# get all artist albums
artist_albums = spotify.artist_albums(artist.get('uri'), limit=50)

# get all albums from artists
albums = artist_albums.get('items')

# open file
f = open('artists.json', 'w')

for album in albums:
    if 'US' not in album.get('available_markets'):
        continue

    # album good information
    album_tracks = spotify.album_tracks(album.get('uri'))
    album_id = album.get('id')
    album_name = album.get('name').replace(' (Remastered)', '')
    album_type = album.get('type')
    album_image = album.get('images')[0].get('url')

    # get album tracks
    tracks = album_tracks.get('items')
    for track in tracks:
        track_id = track.get('id')
        track_name = track.get('name').split(' -')[0].strip()
        track_disc_number = track.get('disc_number')
        track_duration = track.get('duration_ms')
        track_explicit = track.get('explicit')
        track_number = track.get('track_number')

        try:
            track_lyrics = lyrics.getLyrics(artist_name, track_name)
        except ValueError:
            track_lyrics = 'not found'
            continue

        line = dict(artist_name=artist_name, album_id=album_id, album_name=album_name, album_type=album_type,
                    album_image=album_image, track_id=track_id, track_name=track_name,
                    track_disc_number=track_disc_number, track_duration=track_duration, track_explicit=track_explicit,
                    track_number=track_number, track_lyrics=track_lyrics)
        f.write(json.dumps(line) + '\n')
f.close()
