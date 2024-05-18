
class Query:
    def __init__(self, song_database, index_wordsearch, index_titlesearch=None):
        self.song_database = song_database
        self.index_wordsearch = index_wordsearch
        self.index_titlesearch = index_titlesearch

    def query_lyrics(self, user_query):
        self._execute_query(user_query, self.index_wordsearch)

    # def query_lyrics_titles(self, user_query):
        # if self.index_titlesearch is not None:
            # self._execute_query_dual_index(user_query, self.index_wordsearch, self.index_titlesearch)
        # else:
            # print("Title search index not provided.")

    def _execute_query(self, user_query, index):
        # Split the user's query into individual words
        query_words = user_query.split()

        # Initialize a set to store the IDs of the songs that contain all query words
        result_songs = set()

        # Initialize a flag to track if any songs have been found
        songs_found = False

        # Iterate over each word in the query
        for word in query_words:
            # Check if the word is in the inverted index
            if word in index.index:
                # Retrieve the songs containing the word from the inverted index
                songs_with_word = index.index[word]
                # If no songs have been found yet, add all songs containing this word to the result set
                if not result_songs:
                    result_songs.update(song.song_ID for song in songs_with_word)
                else:
                    # Take the intersection of the current result set and the songs containing this word
                    result_songs.intersection_update(song.song_ID for song in songs_with_word)

        # If no songs were found, display a message
        if not result_songs:
            print("No songs found matching the query.")
        else:
            # Display the titles and artists of the matching songs
            print("Matching songs:", len(result_songs))
            for song in self.song_database:
                if song.song_ID in result_songs:
                    print(f"- '{song.title}' by {song.artist}")
                    songs_found = True
            # Display all the information including full lyrics
            # for song in self.song_database:
                # if song.song_ID in result_songs:
                    # print("\n")
                    # song.display()
                    # songs_found = True

            # If no songs were found, display a message
            if not songs_found:
                print("No songs found matching all words in the query.")

    # def _execute_query_dual_index(self, user_query, index_lyrics, index_titles):
