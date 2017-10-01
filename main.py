import re
from collections import Counter


class Stat:
    def __init__(self):
        self.d = {}

    def add(self, two_letters, letter):
        counter = self.d.get(two_letters, None)

        if counter is None:
            counter = Counter()
            self.d[two_letters] = counter

        counter[letter] += 1


class Profile:
    def __init__(self):

        self.pattern = re.compile('[A-Za-z]+')

        self.first = Stat()
        self.second = Stat()
        self.middle = Stat()
        self.prelast = Stat()
        self.last = Stat()

    def update_by_sentence(self, sentence):
        words = self.pattern.findall(sentence)
        for word in words:
            self.update(word)

    def update(self, word):
        l = len(word)
        if l > 3:
            word = word.lower()
            for i in range(l):
                c = word[i]
                if i == 0:
                    pass


with open('data/list907.tsv') as f:
    lines = f.readlines()

    for l in lines:
        pass