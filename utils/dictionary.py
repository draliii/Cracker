import pickle as pkl
import numpy as np


def make_dictionary(file, outfile):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                "V", "W", "X", "Y", "Z"]

    word_dict = {}
    letters = {}
    bigrams = {}
    trigrams = {}
    n_letters = 10
    n_words = 10

    for i in alphabet:
        letters[i] = 0
        for j in alphabet:
            bigrams[i + j] = 0
            for k in alphabet:
                trigrams[i + j + k] = 0

    with open(file) as f:
        words = f.readline()
        N_words = len(words.split(" "))
        for w in words.split(" "):
            if w not in word_dict:
                word_dict[w] = 1
            else:
                word_dict[w] += 1

        raw_text = words.replace(" ", "")
        n_letters = len(raw_text)

        N = len(raw_text)
        for i in range(0, N-3):
            letters[raw_text[i]] += 1
            bigrams[raw_text[i] + raw_text[i+1]] += 1
            trigrams[raw_text[i] + raw_text[i+1] + raw_text[i+2]] += 1

        letters[raw_text[N - 2]] += 1
        letters[raw_text[N - 3]] += 1
        bigrams[raw_text[N - 3] + raw_text[N - 2]] += 1

    lv = list(letters.values())
    ic = 26*np.sum(np.multiply(lv, np.subtract(lv, 1))) / (n_letters * (n_letters - 1))

    word_dict_values = list(word_dict.values())
    word_dict_values = np.divide(word_dict_values, N_words)
    word_dict = dict(zip(word_dict.keys(), word_dict_values))

    letters_values = list(letters.values())
    letters_values = np.divide(letters_values, n_letters)
    letters = dict(zip(letters.keys(), letters_values))

    bigrams_values = list(bigrams.values())
    bigrams_values = np.divide(bigrams_values, n_letters - 1)
    bigrams = dict(zip(bigrams.keys(), bigrams_values))

    trigrams_values = list(trigrams.values())
    trigrams_values = np.divide(trigrams_values, n_letters - 2)
    trigrams = dict(zip(trigrams.keys(), trigrams_values))

    dictionary = (word_dict, letters, bigrams, trigrams, ic)
    pkl.dump(dictionary, open(outfile, "wb"))


if __name__ == "__main__":
    make_dictionary("cs-krakatit.txt", "cs.pkl")
    make_dictionary("en-robin-hood.txt", "en.pkl")
