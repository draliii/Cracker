import numpy as np


def compute_score(text, dictionary, f=True, bi=True, tri=True):
    stats = TextStats(text)
    f_score = 0
    bi_score = 0
    tri_score = 0

    if f:
        f_score = np.sum(np.multiply(stats.frequency, dictionary.frequency))
    if bi:
        bi_score = np.sum(np.multiply(stats.bigrams, dictionary.bigrams))
    if tri:
        tri_score = np.sum(np.multiply(stats.trigrams, dictionary.trigrams))

    return f_score + bi_score + tri_score


class TextStats():
    def __init__(self, text):
        self.text = text.replace(" ", "")
        self.N = len(self.text)

        self.ic, self.histogram, self.frequency, self.bigrams, self.bigram_keys, self.trigrams,\
        self.trigram_keys = compute_ngrams(self.text, self.N)


def compute_ngrams(text, N=None):
    text = text.replace(" ", "")

    if N is None:
        N = len(text)

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y", "Z"]
    letters = []
    bigrams = []
    bigram_keys = []
    trigrams = []
    trigram_keys = []

    for i in alphabet:
        letters.append(0)
        for j in alphabet:
            bigrams.append(0)
            bigram_keys.append(i + j)
            for k in alphabet:
                trigrams.append(0)
                trigram_keys.append(i + j + k)

    for i in range(0, N-3):
        I = ord(text[i]) - 65
        J = ord(text[i+1]) - 65
        K = ord(text[i+2]) - 65

        letters[I] += 1
        bigrams[26*I + J] += 1
        trigrams[26*26*I + 26*J + K] += 1

    I = ord(text[N - 3]) - 65
    J = ord(text[N - 2]) - 65
    letters[I] += 1
    letters[J] += 1
    bigrams[26*I + J] += 1

    ic = 26*np.sum(np.multiply(letters, np.subtract(letters, 1))) / (N * (N - 1))

    frequency = np.divide(letters, N)
    bigrams = np.divide(bigrams, N - 1)
    trigrams = np.divide(trigrams, N - 2)

    return ic, letters, frequency, bigrams, bigram_keys, trigrams, trigram_keys


if __name__ == "__main__":
    text = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECH"
    stats = TextStats(text)
    print(stats.ic)

