import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values

scope = 'user-library-read,user-library-modify'

env = ".env.local"
config = dotenv_values(env)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config["SPOTIFY_CLIENT_ID"],
    client_secret=config["SPOTIFY_CLIENT_SECRET"],
    redirect_uri=config["SPOTIFY_REDIRECT_URI"],
    scope=scope))

def remove_tracks(results):
    """ If saved tracks contains the tracks in results, delete them """
    # Get list of track IDs from result of tracks
    track_ids = [item['track']['id'] for item in results['items']]
    if sp.current_user_saved_tracks_contains(track_ids):
        results = sp.current_user_saved_tracks_delete(track_ids)

results = sp.current_user_saved_tracks()
remove_tracks(results)

while results['next']:
    results = sp.next(results)
    remove_tracks(results)
