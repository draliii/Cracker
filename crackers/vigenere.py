from itertools import combinations_with_replacement as combinations
import numpy as np
import pickle as pkl
from utils.text_analyzer import TextStats, compute_score
from utils.dictionary import Dictionary
from crackers.mono import rot


def crack_vigenere(stats: TextStats, dictionary: Dictionary, n_best: int=3, key_limit: int=10, verbose: bool=False):
    output_texts = []
    for key_len in range(2, key_limit):
        if verbose:
            print(key_len)
        filler_size = stats.N % key_len
        if filler_size:
            text = stats.text[0:-filler_size]
        else:
            text = stats.text

        m = int(len(text) / key_len)
        f = np.array(list(text))
        cipher_table = np.transpose(np.reshape(f, (m, key_len)))
        candidates = []

        for line_id in range(0, key_len):
            line_data = "".join(cipher_table[line_id, :])

            line_candidates = []

            for shift in range(0, 26):
                if shift == 22:
                    k = 3
                shifted_line = rot(line_data, shift)
                shifted_score = compute_score(shifted_line, dictionary, bi=0, tri=0)
                line_candidates.append((shifted_score, (26-shift)%26, shifted_line))

            line_candidates.sort(key=lambda c: c[0], reverse=True)

            candidates.append(line_candidates)

        possible_candidate_ids = list(range(0, n_best))

        output_texts_for_keylen = []
        for combination in combinations(possible_candidate_ids, key_len):
            plaintext_table = np.zeros(cipher_table.shape)
            key = ""
            for line_id in range(0, key_len):
                key += chr(candidates[line_id][combination[line_id]][1] + 65)
                plaintext_table[line_id] = list(map(ord, list(candidates[line_id][combination[line_id]][2])))

            table = np.reshape(np.transpose(plaintext_table), (1, len(text))).tolist()
            table = table[0]
            for i in range(0, len(table)):
                table[i] = chr(int(table[i]))
            text = "".join(table)
            score = compute_score(text, dictionary)
            output_texts_for_keylen.append((score, combination, key, text))

        output_texts_for_keylen.sort(key=lambda c: c[0], reverse=True)
        for i in range(0, n_best):
            if verbose:
                print(output_texts_for_keylen[i])
            output_texts.append(output_texts_for_keylen[i])

    output_texts.sort(key=lambda c: c[0], reverse=True)
    return output_texts[0]
