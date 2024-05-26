import os
from Class_Database import SongDatabaseBuilder
from Class_Query import Query

DB_FILE = 'song_database.pkl'
INDEX_FILE = 'index_wordsearch.pkl'
INDEX_TITLES = 'index_songtitles'

# Initialize the song database builder
builder = SongDatabaseBuilder("lyrics")

# Check if the files exist
if os.path.exists(DB_FILE) and os.path.exists(INDEX_FILE) and os.path.exists(INDEX_TITLES):
    print("---Loading database and index from files---")
    song_database, index_wordsearch, index_songtitles = builder.load_from_file(DB_FILE, INDEX_FILE, INDEX_TITLES)
else:
    print("---Building database from archive---")
    song_database, index_wordsearch, index_songtitles = builder.build_database()
    builder.save_to_file(song_database, index_wordsearch, index_songtitles, DB_FILE, INDEX_FILE, INDEX_TITLES)

print("\nNumber of songs in this corpus: ", len(song_database))
print("\n")

# Create an instance of the Query class
# query_instance = Query(song_database, index_wordsearch) # search for lyrics only

# search for titles only or both lyrics and titles
query_instance = Query(song_database, index_wordsearch, index_songtitles)

while True:
    user_query = input("Search for words in the lyrics (press 'q' to quit): ")
    if user_query == "q":
        print("Search ended.")
        break

    # Perform the lyrics query using the desired Query class instance
    # query_instance.query_lyrics(user_query)  # search for lyrics only
    # query_instance.query_titles(user_query)  # search for titles only

    # weighted search for both lyrics and titles
    # query_instance.query_complete(user_query)

    # weighted search including mme (<= 2)
    # query_instance.query_with_mme(user_query)

    # weighted search considering word occurances
    query_instance.query_with_word_counts(user_query)
