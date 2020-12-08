#!/usr/bin/python3

import glob
import json

song_in_a_row = {'count': 0}
song_count = 1
song_start = None

artist_in_a_row = {'count': 0}
artist_count = 1
artist_start = None

last_artist = None
last_song = None

first_date = None
total_streams = 0

library = {}
for filename in sorted(glob.glob('./StreamingHistory*.json')):
    # assume these files are sorted by date
    with open(filename) as f:
        tracks = json.load(f)
        total_streams += len(tracks)
        for track in tracks:
            date = track['endTime'].split()[0]
            if date.startswith('2019'):
                # skip anything from 2019
                continue

            first_date = first_date or date

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
            elif last_artist and last_song:
                if song_count > song_in_a_row['count']:
                    song_in_a_row = {
                        'artist': last_artist,
                        'song': last_song,
                        'date': last_date if last_date == song_start else '{} - {}'.format(song_start or first_date, last_date),
                        'count': song_count,
                    }
                song_count = 1
                song_start = date

            # check if artist changed
            if last_artist == artist:
                artist_count += 1
            elif last_artist:
                if artist_count > artist_in_a_row['count']:
                    artist_in_a_row = {
                        'artist': last_artist,
                        'date': last_date if last_date == artist_start else '{} - {}'.format(artist_start or first_date, last_date),
                        'count': artist_count,
                    }
                artist_count = 1
                artist_start = date

            last_artist = artist
            last_song = song
            last_date = date

song_totals = {}
artist_totals = {}
for artist, songs in library.items():
    artist_totals[artist] = {'duration': 0, 'count': 0}
    for song, data in songs.items():
        artist_totals[artist]['duration'] += data['duration']
        artist_totals[artist]['count'] += data['count']

        song_totals[artist, song] = data

print('# Spotify Summary ({} - {})'.format(first_date, last_date))
print()
print('###', total_streams, 'total songs')
print()
print('###', len(song_totals.keys()), 'unique songs')
print()
print('###', len(artist_totals.keys()), 'artists')
print()
print('###', sum({x['duration'] for x in artist_totals.values()}) // 1000 // 60, 'minutes')
print()
print('## Top artists')
print()
print('| Artist | Plays | Time |')
print('| --- | --- | --- |')
for artist, data in sorted(artist_totals.items(), key=lambda x: (x[1]['duration'], x[1]['count']), reverse=True)[:10]:
    plays = data['count']
    ms = data['duration']
    print('| {} | {} | {} min |'.format(artist, plays, ms // 1000 // 60))

print()
print('## Top songs')
print()
print('| Song | Artist | Plays | Time |')
print('| --- | --- | --- | --- |')
for (artist, song), data in sorted(song_totals.items(), key=lambda x: (x[1]['count'], x[1]['duration']), reverse=True)[:10]:
    ms = data['duration']
    count = data['count']
    print('| {} | {} | {} | {} min |'.format(song, artist, count, ms // 1000 // 60))
print()

print('## Artist played most in a row')
print()
print('{}, {} times ({})'.format(artist_in_a_row['artist'], artist_in_a_row['count'], artist_in_a_row['date']))

print()
print('## Song played most in a row')
print()
print('{} by {}, {} times ({})'.format(song_in_a_row['song'], song_in_a_row['artist'], song_in_a_row['count'], song_in_a_row['date']))
