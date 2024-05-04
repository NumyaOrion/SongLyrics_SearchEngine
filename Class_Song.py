class Song:
    # Class variable to keep track of the song index
    song_index = 0

    def __init__(self, artist, title, lyrics):
        self.artist = artist
        self.title = title
        self.song_ID = Song.song_index  # Assign the current song index as the ID
        self.lyrics = lyrics

        # Increment the song index for the next song
        Song.song_index += 1

    def display(self):
        print(f"Artist: {self.artist}")
        print(f"Title: {self.title}")
        print(f"ID: {self.song_ID}")
        print("Lyrics:")
        print(self.lyrics)
        print()
