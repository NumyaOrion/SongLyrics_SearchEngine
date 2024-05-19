import os
import pickle
from Class_Song import Song
from Class_Indices import InvertedIndexWords
from Class_Indices import InvertedIndexTitle


class SongDatabaseBuilder:  # receives directory, builds + gives back database (list of dict)
    def __init__(self, directory):
        self.directory = directory

    def build_database(self):
        song_database = []
        inverted_index_wordsearch = InvertedIndexWords()
        inverted_index_songtitles = InvertedIndexTitle()

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

                            # Update the inverted index for the lyrics
                            inverted_index_wordsearch.add_song(song)
                            # Update the inverted index for the song titles
                            inverted_index_songtitles.add_title(song)

        return song_database, inverted_index_wordsearch, inverted_index_songtitles

    def save_to_file(self, song_database, index_wordsearch, index_songtitles, db_file, index_file, index_titles_file):
        with open(db_file, 'wb') as dbf:
            pickle.dump(song_database, dbf)
        with open(index_file, 'wb') as idxf:
            pickle.dump(index_wordsearch, idxf)
        with open(index_titles_file, 'wb') as idxtf:
            pickle.dump(index_songtitles, idxtf)

    def load_from_file(self, db_file, index_file, index_titles_file):
        with open(db_file, 'rb') as dbf:
            song_database = pickle.load(dbf)
        with open(index_file, 'rb') as idxf:
            index_wordsearch = pickle.load(idxf)
        with open(index_titles_file, 'rb') as idxtf:
            index_songtitles = pickle.load(idxtf)
        return song_database, index_wordsearch, index_songtitles
