class InvertedIndexWords:
    def __init__(self):
        self.index = {}

    def add_song(self, song):
        words = song.lyrics.lower().split()  # Splitting the lyrics string
        for word in words:
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(song)


# TO DO
class InvertedIndexTitle:
    def __init__(self):
        self.index = {}

    def add_title(self, song):
        words = song.title.lower().split()  # Splitting the title string
        for word in words:
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(song)
