import pickle as pkl
import numpy as np


class Dictionary:
    def __init__(self, file: str):
        self.word_dict = {}

        with open(file) as f:
            words = f.readline()
            N_words = len(words.split(" "))
            for w in words.split(" "):
                if w not in self.word_dict:
                    self.word_dict[w] = 1
                else:
                    self.word_dict[w] += 1

            word_dict_values = list(self.word_dict.values())
            word_dict_values = np.divide(word_dict_values, N_words)
            self.word_dict = dict(zip(self.word_dict.keys(), word_dict_values))

            text = words.replace(" ", "")
            N = len(text)

            self.ic, self.histogram, self.frequency, self.bigrams, self.bigram_keys, self.trigrams, self.trigram_keys = compute_ngrams(text, N)

    def save(self, file):
        pkl.dump(self, open(file, "wb"))


def compute_ngrams(text: str, N=None):
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
    en_dict = Dictionary("en-robin-hood.txt")
    en_dict.save("en.pkl")

    cs_dict = Dictionary("cs-krakatit.txt")
    cs_dict.save("cs.pkl")

    # en2_dict = pkl.load(open("en.pkl", "rb"))
