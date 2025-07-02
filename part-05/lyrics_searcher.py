import os
import json
from lyricsgenius import Genius
from dotenv import load_dotenv

load_dotenv()

class LyricsSearcher:

    def __init__(self):
        self.lyrics = {}
        self.genius_search = Genius(os.getenv("GENIUS_API_CLIENT_ACCESS_TOKEN"), timeout=10)

    def get_lyrics(self, song_name: str, artist: str) -> str:
        song_name = song_name.lower().strip()
        artist = artist.lower().strip()
        if f"{song_name}-{artist}" not in self.lyrics:
            self.lyrics[f"{song_name}_{artist}"] = self.search_lyrics(song_name, artist)
        return self.lyrics[f"{song_name}_{artist}"]
    
    def search_lyrics(self, song_name: str, artist: str) -> str:
        song = self.genius_search.search_song(song_name, artist)

        if song is None:
            return None

        return json.dumps({"lyrics": song.lyrics, "song_name": song.title, "artist": song.artist})


if __name__ == "__main__":
    lyrics_searcher = LyricsSearcher()
    # print(lyrics_searcher.get_lyrics("Hallelujah", "Leonard Cohen"))