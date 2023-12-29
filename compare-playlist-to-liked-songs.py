import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values

# TODO: Should scope change?
scope = 'playlist-read-private,user-library-modify'

env = ".env.local"
config = dotenv_values(env)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config["SPOTIFY_CLIENT_ID"],
    client_secret=config["SPOTIFY_CLIENT_SECRET"],
    redirect_uri=config["SPOTIFY_REDIRECT_URI"],
    scope=scope))

results = sp.current_user_playlists(limit=50)
print("Here are your playlists:")
for i, item in enumerate(results['items']):
    # Add 1 to print so counts from 0
    print("%d %s" % (i+1, item['name']))

# Subtract 1 so indexed from 0
playlist_num = int(input("Which number playlist would you like to compare? ")) - 1

playlist_id = results['items'][playlist_num]['id']

# Get IDs of liked songs in a list
# Max limit of 50 https://developer.spotify.com/documentation/web-api/reference/get-users-saved-tracks
results = sp.current_user_saved_tracks(limit=50)
liked_songs_ids = [item["track"]["id"] for item in results["items"]]
while(results["next"]):
    results = sp.next(results)
    liked_songs_ids += [item["track"]["id"] for item in results["items"]]

# Get IDs of playlist songs in a list
# Max limit of 50 https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks
results = sp.playlist_items(playlist_id, limit=50)
playlist_songs_ids = [item["track"]["id"] for item in results["items"]]
while (results['next']):
    results = sp.next(results)
    playlist_songs_ids += [item["track"]["id"] for item in results["items"]]

only_liked_songs = list(set(liked_songs_ids).difference(playlist_songs_ids))
if (len(only_liked_songs) > 0):
    print("Songs that are liked but not in the playlist")
    # Get tracks 50 at a time (due to max length) then print names
    for i in range(0, len(only_liked_songs), 50):
        results = sp.tracks(only_liked_songs[i:i+50])
        print([track["name"] for track in results["tracks"]])
else:
    print("There are no songs in liked songs that aren't in the playlist")

only_playlist_songs = list(set(playlist_songs_ids).difference(liked_songs_ids))
if (len(only_playlist_songs) > 0):
    print("Songs that are in the playlist but not liked")
    # Get tracks 50 at a time (due to max length) then print names
    for i in range(0, len(only_playlist_songs), 50):
        results = sp.tracks(only_playlist_songs[i:i+50])
        print([track["name"] for track in results["tracks"]])
else:
    print("There are no songs in the playlist that aren't liked")
