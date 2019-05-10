import numpy as np
from utils.dictionary import compute_ngrams, Dictionary


def compute_score(text: str, dictionary: Dictionary, f: int=1, bi: int=1, tri: int=1):
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


def compute_score_for_table(table: list, ciphertext: str, dictionary: Dictionary, f: int=1, bi: int=1, tri: int=1):
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


def add_spaces(text: str):
    result = ""
    lst = list(text)
    for i in range(0, len(lst)):
        if not i % 5:
            result += " "
        result += lst[i]
    return result


def swap(a: str, b: str, text: str):
    text = text.replace(a, b.lower())
    text = text.replace(b, a)
    text = text.replace(b.lower(), b)
    return text


def make_table(t1: list, t2: list):
    table = [-1] * 26
    for c1, c2 in zip(t1, t2):
        l1 = ord(c1) - 65
        l2 = ord(c2) - 65
        table[l1] = l2
    return table
