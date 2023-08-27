import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values

scope = 'user-library-read'

def show_tracks(results):
    for item in results['items']:
        track = item['track']
        print("%32.32s %s" % (track['artists'][0]['name'], track['name']))

env = ".env.local"
config = dotenv_values(env)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config["SPOTIFY_CLIENT_ID"],
    client_secret=config["SPOTIFY_CLIENT_SECRET"],
    redirect_uri=config["SPOTIFY_REDIRECT_URI"],
    scope=scope))

results = sp.current_user_saved_tracks()
show_tracks(results)

while results['next']:
    results = sp.next(results)
    show_tracks(results)
