import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ==== תמלא כאן את הפרטים שלך מה-Spotify Dashboard ====
CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID_HERE"
CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET_HERE"
REDIRECT_URI = "http://localhost:8888/callback"  # or whatever you use
SCOPE = "user-modify-playback-state user-read-playback-state"


def create_spotify_client():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            open_browser=True,  # יפתח אוטומטית דפדפן בפעם הראשונה
        )
    )
    return sp


class SpotifyController:
    def __init__(self):
        self.sp = create_spotify_client()

    def next_track(self):
        print("▶️  Next track")
        self.sp.next_track()

    def previous_track(self):
        print("⏮  Previous track")
        self.sp.previous_track()

    def toggle_play(self):
        playback = self.sp.current_playback()
        if playback and playback.get("is_playing"):
            print("⏸  Pause")
            self.sp.pause_playback()
        else:
            print("▶️  Play")
            self.sp.start_playback()


def main():
    ctrl = SpotifyController()
    print("Connected to Spotify!")
    print("Commands:")
    print("  n = next track")
    print("  b = previous track")
    print("  space = play/pause")
    print("  q = quit")

    while True:
        cmd = input("Enter command (n/b/space/q): ")

        if cmd == "n":
            ctrl.next_track()
        elif cmd == "b":
            ctrl.previous_track()
        elif cmd == " ":
            ctrl.toggle_play()
        elif cmd == "q":
            print("Bye!")
            break
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
