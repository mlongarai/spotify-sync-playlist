import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# -----------------------
# CONFIGURATION
# -----------------------
# How to Use
# 1. Spotify Developer Dashboard
# Go to: Spotify Developer Dashboard (https://developer.spotify.com/dashboard)
# Select your app.
# Edit Redirect URIs and add http://localhost:8888
# 2. Save as spotify_sync_playlist.py
# 3. Run:
# pip install spotipy
# export SPOTIPY_CLIENT_ID='your_client_id'
# export SPOTIPY_CLIENT_SECRET='your_client_secret'
# export SPOTIPY_REDIRECT_URI='http://localhost:8888'
# python spotify_sync_playlist.py

PLAYLIST_NAME = "Meu Rock Bebê"
PLAYLIST_DESCRIPTION = "Synced playlist based on local song list."
SONGS = [
    "1999 - Prince",
    "Act Naturally - The Beatles",
    "Ain’t No Sunshine - Bill Withers",
    "Another Brick in the Wall - Pink Floyd",
    "Are You Gonna Go My Way - Lenny Kravitz",
    "Authority Song - John Mellencamp",
    "Baba O’Riley - The Who",
    "Bad Case of Loving You - Robert Palmer",
    "Band on the Run - Paul McCartney & Wings",
    "Black Water - The Doobie Brothers",
    "Boogie Shoes - KC & The Sunshine Band",
    "Build Me Up Buttercup - The Foundations",
    "Burning Down the House - Talking Heads",
    "Can’t You See - The Marshall Tucker Band",
    "Come Together - The Beatles",
    "Crazy Little Thing Called Love - Queen",
    "Dead Flowers - The Rolling Stones",
    "Devil in Disguise - Elvis Presley",
    "Don’t Bring Me Down - Electric Light Orchestra",
    "Drive My Car - The Beatles",
    "Even the Losers - Tom Petty",
    "Fast as You - Dwight Yoakam",
    "Fool in the Rain - Led Zeppelin",
    "Gimme Shelter - The Rolling Stones",
    "Give Me One Reason - Tracy Chapman",
    "Good Day Sunshine - The Beatles",
    "Good Vibrations - The Beach Boys",
    "Hey Jude - The Beatles",
    "I Got You Babe - Sonny & Cher",
    "I Saw Her Standing There - The Beatles",
    "I Want to Hold Your Hand - The Beatles",
    "I’m a Man - The Spencer Davis Group",
    "I’ve Just Seen a Face - The Beatles",
    "Johnny B. Goode - Chuck Berry",
    "Like a Rolling Stone - Bob Dylan",
    "Listen to the Music - The Doobie Brothers",
    "Lonely Is the Night - Billy Squier",
    "Lovesong - The Cure",
    "Messin’ with the Kid - Junior Wells",
    "Midnight Rambler - The Rolling Stones",
    "Mind Your Own Business - Hank Williams Jr.",
    "Neon Moon - Brooks & Dunn",
    "Nobody to Blame - Chris Stapleton",
    "Oh, Pretty Woman - Roy Orbison",
    "Photograph - Def Leppard",
    "Pride (In the Name of Love) - U2",
    "Ripple - Grateful Dead",
    "Roller Derby Queen - Jim Croce",
    "Runaround Sue - Dion",
    "She Came in Through the Bathroom Window - The Beatles",
    "Soul Man - Sam & Dave",
    "Stand By Me - Ben E. King",
    "Sweet Caroline - Neil Diamond",
    "Taxman - The Beatles",
    "Thank You (Falettinme Be Mice Elf Agin) - Sly & The Family Stone",
    "The Waiting - Tom Petty",
    "Tootie Ma is a Big Fine Thing - Preservation Hall Jazz Band",
    "Treat Her Right - Roy Head",
    "Twist and Shout - The Beatles",
    "Walking on Sunshine - Katrina & The Waves",
    "We Can Work It Out - The Beatles",
    "We Didn’t Start the Fire - Billy Joel",
    "Whip It - Devo",
    "Wonderwall - Oasis",
    "You Can Call Me Al - Paul Simon",
    "You Really Got Me - The Kinks",
    "Cocaine - Eric Clapton",
    "Sunshine of your love - Cream",
    "Sultans of Swing - Dire Straits",
    "Money for Nothing - Single Edit / Remastered 2022 - Dire Straits",
    "Take It Easy - Eagles",
    "Hey Joe - Jimi Hendrix",
    "every breath you take - The Police",
    "Roxanne - The Police",
    "Message in a Bottle - The Police",
    "Every Little Thing She Does Is Magic - The Police",
    "Have you ever seen the rain - Creedence Clearwater Revival",
    "Fortunate Son - Creedence Clearwater Revival",
    "Bad Moon Rising - Creedence Clearwater Revival",
    "Proud Mary - Creedence Clearwater Revival",
    "Up Around The Bend- Creedence Clearwater Revival",
    "Black In Black - AC/DC",
    "Thunderstruck - AC/DC",
    "Highway to Hell - AC/DC",
    "You shook me all night long - AC/DC",
    "Song2 - Blur",
    "Iron Man - Black Sabbath",
    "Enter Sandman - Metallica",
    "Smoke on the Water - Deep Purple",
    "Sweet Child O’ Mine - Guns N’ Roses",
    "Livin’ on a Prayer - Bon Jovi",
    "I Love Rock ‘n’ Roll - Joan Jett & The Blackhearts",
    "Dreams - Fleetwood Mac",
    "In the End - Linkin Park",
    "Should I Stay or Should I Go - The Clash",
    "When I come around - Green Day",
    "Times like these - Foo Fighters",
    "Everlong - Foo Fighters",
    "Bring Me to Life - Evanescence",
    "Wish You Were Here - Pink Floyd",
    "Paranoid - Black Sabbath",
    "Creep - Radiohead",
    "Karma Police - Radiohead",
    "Losing My Religion - R.E.M.",
    "Smells Like Teen Spirit - Nirvana",
    "Seven Nation Army - The White Stripes",
    "Sweet Home Alabama - Lynyrd Skynyrd",
    "Starman - David Bowie",
    "Come Together - The Beatles",
    "Sympathy for the Devil - The Rolling Stones",
    "Lonely Boy - The Black Keys",
    "Tighten Up - The Black Keys",
    "Chop Suey! - System of a Down",
    "Toxicity - System of a Down",
    "Arials - System of a Down",
    "Lonely Day - System of a Down",
    "B.Y.O.B. - System of a Down",
    "You’ve Got to Hide Your Love Away - The Beatles"
]

# -----------------------
# AUTHENTICATION
# -----------------------

scope = "playlist-modify-private playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# -----------------------
# CREATE OR GET PLAYLIST
# -----------------------

user_id = sp.current_user()["id"]

# Check if playlist already exists
playlist_id = None
offset = 0
while True:
    playlists = sp.current_user_playlists(offset=offset)["items"]
    if not playlists:
        break
    for playlist in playlists:
        if playlist["name"] == PLAYLIST_NAME:
            playlist_id = playlist["id"]
            break
    if playlist_id or len(playlists) < 50:
        break
    offset += 50

# Create if not found
if not playlist_id:
    playlist = sp.user_playlist_create(user=user_id, name=PLAYLIST_NAME, public=False, description=PLAYLIST_DESCRIPTION)
    playlist_id = playlist["id"]
    print(f"✅ Created playlist: {PLAYLIST_NAME}")
else:
    print(f"✅ Found existing playlist: {PLAYLIST_NAME}")

# -----------------------
# SEARCH DESIRED TRACKS
# -----------------------

desired_track_ids = []
for song in SONGS:
    result = sp.search(q=song, type='track', limit=1)
    items = result.get('tracks', {}).get('items', [])
    if items:
        track_id = items[0]['id']
        desired_track_ids.append(track_id)
        print(f"✅ Found: {song} -> {items[0]['name']} – {items[0]['artists'][0]['name']}")
    else:
        print(f"❌ Not found: {song}")

# -----------------------
# GET EXISTING PLAYLIST TRACKS
# -----------------------

existing_track_ids = []
offset = 0
while True:
    response = sp.playlist_items(playlist_id, offset=offset, fields="items.track.id,total", additional_types=["track"])
    items = response['items']
    if not items:
        break
    existing_track_ids.extend([item['track']['id'] for item in items if item['track']])
    offset += len(items)

# -----------------------
# SYNC PLAYLIST
# -----------------------

to_add = list(set(desired_track_ids) - set(existing_track_ids))
to_remove = list(set(existing_track_ids) - set(desired_track_ids))

if to_remove:
    print(f"🗑 Removing {len(to_remove)} tracks...")
    sp.playlist_remove_all_occurrences_of_items(playlist_id, to_remove)

if to_add:
    print(f"➕ Adding {len(to_add)} tracks...")
    for i in range(0, len(to_add), 100):
        sp.playlist_add_items(playlist_id, to_add[i:i+100])

print("🎵 Playlist sync complete.")
print(f"🔗 https://open.spotify.com/playlist/{playlist_id}")
