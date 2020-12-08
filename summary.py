#!/usr/bin/python3

import json

# assume these files are sorted by date
files = (
    'StreamingHistory0.json',
    'StreamingHistory1.json',
    'StreamingHistory2.json',
)

song_in_a_row = {'count': 0}
artist_in_a_row = {'count': 0}
song_count = 1
artist_count = 1
last_artist = None
last_song = None

print('2020 Spotify Summary (1 Jan - 4 Dec)')
library = {}
for filename in files:
    with open(filename) as f:
        tracks = json.load(f)
        for track in tracks:
            last_date = track['endTime'].split()[0]
            if last_date.startswith('2019'):
                # skip anything from 2019
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

            # check is song or artist changed
            if last_artist == artist and last_song == song:
                song_count += 1
            else:
                if song_count > song_in_a_row['count']:
                    song_in_a_row = {
                        'artist': last_artist,
                        'song': last_song,
                        'date': last_date,
                        'count': song_count,
                    }
                song_count = 1

            # check if artist changed
            if last_artist == artist:
                artist_count += 1
            else:
                if artist_count > artist_in_a_row['count']:
                    artist_in_a_row = {
                        'artist': last_artist,
                        'date': last_date,
                        'count': artist_count,
                    }
                artist_count = 1

            last_artist = artist
            last_song = song
            last_date = last_date

song_totals = {}
artist_totals = {}
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
for (artist, song), data in sorted(song_totals.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
    ms = data['duration']
    count = data['count']
    print('{:<30} {:<20} {:>3} times, {:>5} min'.format(song, artist, count, ms // 1000 // 60))

print()
print('Artist played most in a row:')
print('    {}'.format(artist_in_a_row['artist']))
print('    {} times on {}'.format(artist_in_a_row['count'], artist_in_a_row['date']))

print()
print('Song played most in a row:')
print('    {}'.format(song_in_a_row['song']))
print('    {}'.format(song_in_a_row['artist']))
print('    {} times on {}'.format(song_in_a_row['count'], song_in_a_row['date']))
