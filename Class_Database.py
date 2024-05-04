import os
from Class_Song import Song
from Class_Indices import InvertedIndexWords
from Class_Indices import InvertedIndexTitle


class SongDatabaseBuilder:  # receives directory, builds + gives back database (list of dict)
    def __init__(self, directory):
        self.directory = directory

    def build_database(self):
        song_database = []
        inverted_index_wordsearch = InvertedIndexWords()

        # Iterate over each artist's folder
        for artist_folder in os.listdir(self.directory):
            artist_folder_path = os.path.join(self.directory, artist_folder)

            # Check if the item in the directory is a directory (artist folder)
            if os.path.isdir(artist_folder_path):
                # Iterate over each .txt file in the artist's folder
                for file_name in os.listdir(artist_folder_path):
                    if file_name.endswith(".txt"):  # Check if the file is a .txt file
                        file_path = os.path.join(artist_folder_path, file_name)

                        # Remove the ".txt" extension from the file name to get the song title
                        title = os.path.splitext(file_name)[0]

                        with open(file_path, "r", encoding="utf-8") as f:
                            # Read the lyrics from the file
                            lyrics = f.read()

                            # Create a Song object
                            song = Song(artist_folder, title, lyrics)

                            # Append the song to the song_database list
                            song_database.append(song)

                            # Update the inverted index
                            inverted_index_wordsearch.add_song(song)

        return song_database, inverted_index_wordsearch
