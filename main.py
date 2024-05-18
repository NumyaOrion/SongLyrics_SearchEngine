# import json
import os
from Class_Database import SongDatabaseBuilder
from Class_Query import Query
# from Class_Song import Song

DB_FILE = 'song_database.pkl'
INDEX_FILE = 'index_wordsearch.pkl'

# Build the song database
builder = SongDatabaseBuilder("lyrics")

# Check if the files exist
if os.path.exists(DB_FILE) and os.path.exists(INDEX_FILE):
    print("---Loading database and index from files---")
    song_database, index_wordsearch = builder.load_from_file(DB_FILE, INDEX_FILE)
else:
    print("---Building database from archive---")
    song_database, index_wordsearch = builder.build_database()
    builder.save_to_file(song_database, index_wordsearch, DB_FILE, INDEX_FILE)

print("\nNumber of songs in this corpus: ", len(song_database))
print("\n")

# Create an instance of the Query class
query_instance = Query(song_database, index_wordsearch)

while True:
    user_query = input("Search for words in the lyrics (press 'q' to quit): ")
    if user_query == "q":
        print("Search ended.")
        break

    # Perform the lyrics query using the Query class instance
    query_instance.query_lyrics(user_query)
