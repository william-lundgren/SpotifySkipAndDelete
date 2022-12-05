import spotipy
import pygame as pg
from spotipy.oauth2 import SpotifyOAuth


class App:
    def __init__(self, id_num, secret):
        # For getting the current playing track, removing track from playlist and skipping to next song
        self.scope = "playlist-modify-private,user-read-currently-playing,user-modify-playback-state"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id_num,
                                                            client_secret=secret,
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
    with open("client_id.txt", "r") as f:
        id_num = f.readline()
    with open("client_secret.txt", "r") as f:
        secret = f.readline()
    app = App(id_num, secret)
    pg.init()
    print(app.sp.currently_playing())
    pg.display.set_caption("Skip and delete")
    display = pg.display.set_mode((200, 200))
    clock = pg.time.Clock()
    game_exit = False

    while not game_exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                app.delete_skip()

        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
