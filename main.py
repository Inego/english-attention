import pickle
import re
from collections import Counter

from os.path import isfile

PICKLED_PROFILE_PATH = 'data/profile.p'
LIST_907_PATH = 'data/list907.tsv'


class Stat(object):
    def __init__(self):
        self.d = {}

    def add(self, letter, two_letters):
        counter = self.d.get(two_letters, None)

        if counter is None:
            counter = Counter()
            self.d[two_letters] = counter

        counter[letter] += 1

    def get_variants(self, l1, l2, skip=None):
        two_letters = (l1, l2)

        if two_letters not in self.d:
            return []

        c = self.d[two_letters]

        if skip is None:
            return [(k, v) for k, v in c.items()]
        else:
            return [(k, v) for k, v in c.items() if k != skip]


class Profile(object):
    def __init__(self):

        self.pattern = re.compile('[A-Za-z]+')

        self.first = Stat()
        self.second = Stat()
        self.middle = Stat()
        self.pre_last = Stat()
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
                    self.pre_last.add(c, (w[l - 3], w[l - 1]))
                elif i == l - 1:
                    self.last.add(c, (w[l - 3], w[l - 2]))
                else:
                    self.middle.add(c, (w[i - 1], w[i + 1]))

    def get_additions(self, w):
        l = len(w)
        if l < 3:
            return []

        result = []

        for i in range(l + 1):
            if i == 0:
                stat_variants = self.first.get_variants(w[0], w[1])
            elif i == 1:
                stat_variants = self.second.get_variants(w[0], w[1])
            elif i == l:
                stat_variants = self.last.get_variants(w[l-2], w[l-1])
            elif i == l - 1:
                stat_variants = self.pre_last.get_variants(w[l-2], w[l-1])
            else:
                stat_variants = self.middle.get_variants(w[i-1], w[i])

            position_result = []

            for variant in stat_variants:
                position_result.append((w[:i] + variant[0] + w[i:], variant[1]))

            if position_result:
                result.append(position_result)

        return result


def get_sentences():
    with open(LIST_907_PATH, encoding='utf-8') as f:
        print("Reading lines...")
        return f.readlines()


def gather_from_907():
    print("Gathering profile from list 907...")

    result = Profile()

    lines = get_sentences()

    print("Iterating lines...")
    for i, l in enumerate(lines):
        if i % 10000 == 0:
            print(i)

        result.update_by_sentence(l)

    with open(PICKLED_PROFILE_PATH, 'wb') as f:
        pickle.dump(result, f)

    return result


def get_profile() -> Profile:
    if isfile(PICKLED_PROFILE_PATH):
        with open(PICKLED_PROFILE_PATH, 'rb') as f:
            return pickle.load(f)
    else:
        return gather_from_907()


# =================================
p = get_profile()

a = p.get_additions('song')

print(a)