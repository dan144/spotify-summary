#!/usr/bin/python3

import json

files = (
    'StreamingHistory0.json',
    'StreamingHistory1.json',
    'StreamingHistory2.json',
)

library = {}
last_artist = None
last_song = None
for filename in files:
    with open(filename) as f:
        tracks = json.load(f)
        for track in tracks:
            if track['endTime'].startswith('2019'):
                continue
            if track['endTime'].startswith('2020-12') or track['endTime'].startswith('2020-11'):
                continue

            artist = track['artistName']
            song = track['trackName']
            ms = track['msPlayed']
            if artist not in library:
                library[artist] = {}
            if song not in library[artist]:
                library[artist][song] = 0
            library[artist][song] += ms
            last_artist = track['artistName']
            last_song = track['trackName']
            # library[artist][track] += ms

totals = {}
for artist, songs in library.items():
    totals[artist] = 0
    for song, ms in songs.items():
        totals[artist] += ms

for artist, ms in sorted(totals.items(), key=lambda x: x[1]):
    print(artist, ms // 1000 // 60)

print('Total:', sum(totals.values()) // 1000 // 60)
