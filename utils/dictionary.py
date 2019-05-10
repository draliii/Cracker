import pickle as pkl
import numpy as np
from utils.text_analyzer import compute_ngrams


class Dictionary:
    def __init__(self, file):
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


if __name__ == "__main__":
    en_dict = Dictionary("en-robin-hood.txt")
    en_dict.save("en.pkl")

    cs_dict = Dictionary("cs-krakatit.txt")
    cs_dict.save("cs.pkl")

    # en2_dict = pkl.load(open("en.pkl", "rb"))
