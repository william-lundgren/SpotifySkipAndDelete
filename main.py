import spotipy
import pygame as pg
from spotipy.oauth2 import SpotifyOAuth


class App:

    def __init__(self):
        # For getting the current playing track, removing track from playlist and skipping to next song
        self.scope = "user-read-currently-playing,playlist-modify-private,user-modify-playback-state"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ebc656c4e7ee4e2280a2b0b0f1410d10",
                                                       client_secret="4b5eed7800f940ed8aef228f0f43a8ea",
                                                       redirect_uri="http://localhost",
                                                       scope=self.scope))

    def delete_skip(self):
        results = self.sp.currently_playing()
        playlist_uri = results["context"]["uri"]
        track_id = results["item"]["uri"]
        self.sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_uri, items=[track_id])
        self.sp.next_track()
        print("SKIPPED AND DELETED")


def main():
    app = App()

    pg.init()
    pg.display.set_caption("Skip and delete")
    display = pg.display.set_mode((200,200))
    clock = pg.time.Clock()
    game_exit = False

    while not game_exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                print("TRUE")
                app.delete_skip()

        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()