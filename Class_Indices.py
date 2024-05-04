# ISSUES TO SOLVE:
# - Second index for titles
# - write index and database to file
# - weight index title and word differently, display only a specific amount of results

class InvertedIndexWords:
    def __init__(self):
        self.index = {}

    def add_song(self, song):
        words = song.lyrics.split()  # Splitting the lyrics string
        for word in words:
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(song)


# TO DO
class InvertedIndexTitle:
    def __init__(self):
        self.index = {}

    def add_title(self, song):
        words = song.title.split()  # Splitting the title string
        for word in words:
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(song)
