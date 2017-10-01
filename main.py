import pickle
import re
from collections import Counter


class Stat(object):
    def __init__(self):
        self.d = {}

    def add(self, letter, two_letters):
        counter = self.d.get(two_letters, None)

        if counter is None:
            counter = Counter()
            self.d[two_letters] = counter

        counter[letter] += 1


class Profile(object):
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

    def update(self, w):
        l = len(w)
        if l > 3:
            w = w.lower()
            for i in range(l):
                c = w[i]
                if i == 0:
                    self.first.add(c, (w[1], w[2]))
                elif i == 1:
                    self.second.add(c, (w[0], w[2]))
                elif i == l - 2:
                    self.prelast.add(c, (w[l-3], w[l-1]))
                elif i == l - 1:
                    self.last.add(c, (w[l-3], w[l-2]))
                else:
                    self.middle.add(c, (w[i-1], w[i+1]))


def gather_from_907():

    print("Gathering profile from list 907...")

    p = Profile()

    with open('data/list907.tsv') as f:
        print("Reading lines...")
        lines = f.readlines()

        print("Iterating lines...")
        for i, l in enumerate(lines):
            if i % 10000 == 0:
                print(i)

            p.update_by_sentence(l)

    with open('data/profile.p', 'wb') as f:
        pickle.dump(p, f)


# =================================
gather_from_907()
