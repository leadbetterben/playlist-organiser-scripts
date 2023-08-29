import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import dotenv_values

scope = 'playlist-read-private'

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
playlist_num = int(input("Which number playlist would you like to save the songs of? ")) - 1

playlist_id = results['items'][playlist_num]['id']
