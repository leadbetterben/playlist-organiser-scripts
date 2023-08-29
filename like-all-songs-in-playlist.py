import spotipy
from spotipy.oauth2 import SpotifyOAuth
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
for i, item in enumerate(results['items']):
    print("%d %s" % (i, item['name']))
