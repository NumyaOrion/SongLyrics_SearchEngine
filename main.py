# import json
# import os
from Class_Database import SongDatabaseBuilder
from Class_Query import Query
# from Class_Song import Song


# Build the song database
builder = SongDatabaseBuilder("lyrics")
song_database, index_wordsearch = builder.build_database()
print("---Database built from archive---")

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
