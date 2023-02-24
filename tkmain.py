import tkinter as tk
from spotipy.oauth2 import SpotifyOAuth
import spotipy


class App(tk.Frame):
    def __init__(self, id_num, secret):
        self.root = tk.Tk()
        self.root.geometry("200x200")
        tk.Frame.__init__(self, self.root)

        # For getting the current playing track, removing track from playlist and skipping to next song
        self.scope = "playlist-modify-private,user-read-currently-playing,user-modify-playback-state"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id_num,
                                                            client_secret=secret,
                                                            redirect_uri="http://localhost",
                                                            scope=self.scope))
        self.root.bind("<Return>", self.delete_skip)
        self.root.overrideredirect(True)
        self.root.overrideredirect(False)
        self.root.wm_attributes("-topmost", "true")

    def delete_skip(self, event):
        results = self.sp.currently_playing()
        playlist_uri = results["context"]["uri"]
        track_id = results["item"]["uri"]
        self.sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_uri, items=[track_id])
        self.sp.next_track()
        with open("skipped.txt", "a") as file:
            file.write(f'{results["item"]["name"]}, {results["item"]["artists"][0]["name"]}\n')
        # print("SKIPPED AND DELETED")


def main():
    with open("client_id.txt", "r") as f:
        id_num = f.readline()
    with open("client_secret.txt", "r") as f:
        secret = f.readline()
    app = App(id_num, secret)
    app.root.mainloop()


if __name__ == "__main__":
    main()
