import numpy as np
from utils.dictionary import compute_ngrams


def compute_score(text: str, dictionary, f=1, bi=1, tri=1):
    stats = TextStats(text)
    f_score = 0
    bi_score = 0
    tri_score = 0

    if f > 0:
        f_score = np.sum(np.multiply(stats.frequency, dictionary.frequency))
    if bi > 0:
        bi_score = np.sum(np.multiply(stats.bigrams, dictionary.bigrams))
    if tri > 0:
        tri_score = np.sum(np.multiply(stats.trigrams, dictionary.trigrams))

    return f*f_score + bi*bi_score + tri*tri_score


def compute_score_for_table(table: list, ciphertext: str, dictionary, f=1, bi=1, tri=1):
    text = ""
    for c in ciphertext:
        text += chr(table[ord(c) - 65] + 65)

    return compute_score(text, dictionary, f, bi, tri), text


class TextStats():
    def __init__(self, text):
        self.text = text.replace(" ", "")
        self.N = len(self.text)

        self.ic, self.histogram, self.frequency, self.bigrams, self.bigram_keys, self.trigrams,\
        self.trigram_keys = compute_ngrams(self.text, self.N)


def add_spaces(text):
    result = ""
    lst = list(text)
    for i in range(0, len(lst)):
        if not i % 5:
            result += " "
        result += lst[i]
    return result


if __name__ == "__main__":
    text = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECH"
    stats = TextStats(text)
    print(stats.ic)

