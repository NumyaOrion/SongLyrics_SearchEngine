
class Query:
    def __init__(self, song_database, index_wordsearch, index_titlesearch=None):
        self.song_database = song_database
        self.index_wordsearch = index_wordsearch
        self.index_titlesearch = index_titlesearch
        self.unique_words = self.get_unique_words_from_indices(index_wordsearch, index_titlesearch)

    def query_lyrics(self, user_query):
        self._execute_query_lyrics(user_query, self.index_wordsearch)

    def query_titles(self, user_query):
        self._execute_query_titles(user_query, self.index_titlesearch)

    def query_complete(self, user_query):
        self._execute_query_complete(user_query, self.index_wordsearch, self.index_titlesearch)

    def query_with_mme(self, user_query):
        self._execute_query_with_mme(user_query, self.index_wordsearch, self.index_titlesearch)

    def _execute_query_lyrics(self, user_query, index):
        # Split the user's query into individual words
        query_words = user_query.lower().split()

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

    def _execute_query_titles(self, user_query, index):
        # Split the user's query into individual words
        query_words = user_query.lower().split()

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

    def _execute_query_complete(self, user_query, index_lyrics, index_titles):
        # Split the user's query into individual words
        query_words = user_query.lower().split()

        # Retrieve songs that contain the words of the query in the lyrics and store in set
        result_songslyrics = set()

        # Retrieve songs that contain the words of the query in the title and store in set
        result_songtitles = set()

        # Initialize a flag to track if any songs have been found
        songs_found = False

        # Search for query words in the lyrics
        for word in query_words:
            if word in index_lyrics.index:
                songs_with_word = index_lyrics.index[word]
                if not result_songslyrics:
                    result_songslyrics.update(song.song_ID for song in songs_with_word)
                else:
                    result_songslyrics.intersection_update(song.song_ID for song in songs_with_word)

        # Search for query words in the titles
        for word in query_words:
            if word in index_titles.index:
                songs_with_word = index_titles.index[word]
                if not result_songtitles:
                    result_songtitles.update(song.song_ID for song in songs_with_word)
                else:
                    result_songtitles.intersection_update(song.song_ID for song in songs_with_word)

        # Bring the results together and weight them
        final_results = {}
        for song_id in result_songslyrics:
            if song_id in result_songtitles:
                final_results[song_id] = 3  # Lyrics and title match
            else:
                final_results[song_id] = 1  # Lyrics only match

        for song_id in result_songtitles:
            if song_id not in final_results:
                final_results[song_id] = 2  # Title only match

        # Sort the results by weight
        sorted_results = sorted(final_results.items(), key=lambda x: x[1], reverse=True)
        # key=lambda x: x[1]
        # specifies that items should be ordered according to x[1] = second element of tuple = weight

        # Display a maximum of the first results of final_results_list
        maximum_displays = 10
        if not sorted_results:
            print("No songs found matching the query.")
        else:
            print("Matching songs:", len(sorted_results))
            for song_id, weight in sorted_results[:maximum_displays]:
                song = next((s for s in self.song_database if s.song_ID == song_id), None)
                if song:
                    print(f"- '{song.title}' by {song.artist} (Weight: {weight})")
                    songs_found = True

            if not songs_found:
                print("No songs found matching all words in the query.")

    def get_unique_words_from_indices(self, *indices):
        unique_words = set()
        for index in indices:
            if index:
                for word in index.index.keys():
                    unique_words.add(word.lower())
        return unique_words

    def edit_distance(self, word1, word2):
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])

        return dp[m][n]

    def find_candidates(self, word, unique_words):
        candidates = []
        for candidate in unique_words:
            if self.edit_distance(word, candidate) <= 2:
                candidates.append(candidate)
        return candidates

    def correct_query(self, query):
        corrected_query = []
        for word in query.split():
            if len(word) > 3:
                candidates = self.find_candidates(word.lower(), self.unique_words)
                if candidates:
                    corrected_query.append(candidates[0])  # Choose the best candidate, e.g., the first one
                else:
                    corrected_query.append(word)
            else:
                corrected_query.append(word)
        return ' '.join(corrected_query)

    def _execute_query_with_mme(self, user_query, index_lyrics, index_titles):
        # Correct the user's query
        corrected_query = self.correct_query(user_query)
        print(f"Corrected Query: {corrected_query}")  # Debug output to see the corrected query

        # Split the corrected query into individual words
        query_words = corrected_query.lower().split()

        # Retrieve songs that contain the words of the query in the lyrics and store in set
        result_songslyrics = set()

        # Retrieve songs that contain the words of the query in the title and store in set
        result_songtitles = set()

        # Initialize a flag to track if any songs have been found
        songs_found = False

        # Search for query words in the lyrics
        for word in query_words:
            if word in index_lyrics.index:
                songs_with_word = index_lyrics.index[word]
                if not result_songslyrics:
                    result_songslyrics.update(song.song_ID for song in songs_with_word)
                else:
                    result_songslyrics.intersection_update(song.song_ID for song in songs_with_word)

        # Search for query words in the titles
        for word in query_words:
            if word in index_titles.index:
                songs_with_word = index_titles.index[word]
                if not result_songtitles:
                    result_songtitles.update(song.song_ID for song in songs_with_word)
                else:
                    result_songtitles.intersection_update(song.song_ID for song in songs_with_word)

        # Bring the results together and weight them
        final_results = {}
        for song_id in result_songslyrics:
            if song_id in result_songtitles:
                final_results[song_id] = 3  # Lyrics and title match
            else:
                final_results[song_id] = 1  # Lyrics only match

        for song_id in result_songtitles:
            if song_id not in final_results:
                final_results[song_id] = 2  # Title only match

        # Sort the results by weight
        sorted_results = sorted(final_results.items(), key=lambda x: x[1], reverse=True)

        # Display a maximum of the first results of final_results_list
        maximum_displays = 10
        if not sorted_results:
            print("No songs found matching the query.")
        else:
            print("Matching songs:", len(sorted_results))
            for song_id, weight in sorted_results[:maximum_displays]:
                song = next((s for s in self.song_database if s.song_ID == song_id), None)
                if song:
                    print(f"- '{song.title}' by {song.artist} (Weight: {weight})")
                    songs_found = True

            if not songs_found:
                print("No songs found matching all words in the query.")
