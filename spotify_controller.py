import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ==== Spotify Dashboard - Please enter here your spotify account ====
CLIENT_ID = "ADD your spotify client ID here"
CLIENT_SECRET = "ADD your spotify client secret here"
REDIRECT_URI = "ADD REDIRECT"
SCOPE = "user-modify-playback-state user-read-playback-state"


def create_spotify_client():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            open_browser=True,  
        )
    )
    return sp


class SpotifyController:
    def __init__(self):
        self.sp = create_spotify_client() 

    def next_track(self, dx=None, vx=None):
        print(f"▶️  Next track    | dx: {dx:+.3f} | vx: {vx:+.3f}")
        self.sp.next_track()

    def previous_track(self, dx=None, vx=None):
        print(f"⏮  Previous track | dx: {dx:+.3f} | vx: {vx:+.3f}")
        self.sp.previous_track()

    def toggle_play(self, dy=None, vy=None):
        playback = self.sp.current_playback()
        is_playing = playback.get("is_playing") if playback else False
        action = "Pause" if is_playing else "Play"
        
        print(f"🔄 {action}        | dy: {dy:+.3f} | vy: {vy:+.3f}")
        
        if is_playing:
            self.sp.pause_playback()
        else:
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
