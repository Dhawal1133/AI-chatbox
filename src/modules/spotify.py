import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = 'bf6b80bb3e18459cb98328c03ff27cb1'
SPOTIPY_CLIENT_SECRET = '8cd1b79e09ae450a94a6a4c29bc92b90'
SPOTIPY_REDIRECT_URI = 'https://open.spotify.com/'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                client_secret=SPOTIPY_CLIENT_SECRET,
                                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                                scope="user-library-read user-read-playback-state user-modify-playback-state"))

def get_active_device():
    """Check if there's an active device for playback."""
    devices = sp.devices()
    if devices['devices']:
        return devices['devices'][0]['id']  # Return the first active device ID
    else:
        return None  # No active devices

def play_song(song_name):
    """Search for a song and play it."""
    active_device = get_active_device()
    if active_device is None:
        return "No active device found. Please make sure you have a device connected to Spotify."

    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_url = track['uri']
        sp.start_playback(uris=[track_url], device_id=active_device)
        return f"Playing {track['name']} by {track['artists'][0]['name']}"
    else:
        return "Song not found."


def pause_song():
    """Pause the currently playing song."""
    sp.pause_playback()
    return "Song paused."

def resume_song():
    """Resume the currently paused song."""
    sp.start_playback()
    return "Resuming song."

def stop_song():
    """Stop the currently playing song."""
    sp.pause_playback()
    return "Song stopped."

def set_volume(volume_percent):
    if 0 <= volume_percent <= 100:
        sp.volume(volume_percent)
        print(f"Volume set to {volume_percent}%")
    else:
        print("Please set volume between 0 and 100.")

def increase_volume(increment=25):
    current_volume = sp.current_playback()['device']['volume_percent']
    new_volume = min(current_volume + increment, 100)  # Make sure volume does not exceed 100%
    set_volume(new_volume)

def decrease_volume(decrement=25):
    current_volume = sp.current_playback()['device']['volume_percent']
    new_volume = max(current_volume - decrement, 0)  # Make sure volume does not go below 0%
    set_volume(new_volume)


def is_music_playing():
    """Check if music is currently playing."""
    try:
        current_playback = sp.current_playback()
        return current_playback and current_playback['is_playing']
    except Exception as e:
        return False







