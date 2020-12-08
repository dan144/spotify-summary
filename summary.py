#!/usr/bin/python3

import json

files = (
    'StreamingHistory0.json',
    'StreamingHistory1.json',
    'StreamingHistory2.json',
)

in_a_row = {'count': 0}
count = 0
last_artist = None
last_song = None

print('2020 Spotify Summary (1 Jan - 4 Dec)')
library = {}
for filename in files:
    with open(filename) as f:
        tracks = json.load(f)
        for track in tracks:
            end_time = track['endTime'].split()[0]
            if end_time.startswith('2019'):
                continue

            artist = track['artistName']
            song = track['trackName']
            ms = track['msPlayed']

            if artist not in library:
                library[artist] = {}
            if song not in library[artist]:
                library[artist][song] = {'count': 0, 'duration': 0}

            library[artist][song]['duration'] += ms
            library[artist][song]['count'] += 1

            if last_artist == artist and last_song == song:
                count += 1
            else:
                if count > in_a_row['count']:
                    in_a_row = {
                        'artist': last_artist,
                        'song': last_song,
                        'date': end_time,
                        'count': count
                    }
                count = 0

            last_artist = artist
            last_song = song
            last_date = end_time

artist_totals = {}
song_totals = {}
for artist, songs in library.items():
    artist_totals[artist] = 0
    for song, data in songs.items():
        artist_totals[artist] += data['duration']
        song_totals[artist, song] = data

print('Total: {} min'.format(sum(artist_totals.values()) // 1000 // 60))

print()
print('Top artists')
for artist, ms in sorted(artist_totals.items(), key=lambda x: x[1], reverse=True)[:10]:
    print('{:<20} {} min'.format(artist, ms // 1000 // 60))

print()
print('Top songs')
for (artist, song), data in sorted(song_totals.items(), key=lambda x: x[1]['duration'], reverse=True)[:10]:
    ms = data['duration']
    count = data['count']
    print('{:<20} {:<30} {:>5} min, {:>3} times'.format(artist, song, ms // 1000 // 60, count))

print()
print('Song played most in a row:')
print('    {}'.format(in_a_row['song']))
print('    {}'.format(in_a_row['artist']))
print('    {} times on {}'.format(in_a_row['count'], in_a_row['date']))
