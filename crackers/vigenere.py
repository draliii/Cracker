from itertools import combinations_with_replacement as combinations
import numpy as np
from utils.text_analyzer import TextStats, compute_score
from utils.dictionary import Dictionary
from crackers.mono import rot


def crack_vigenere(stats: TextStats, dictionary: Dictionary, n_best: int=3, key_limit: int=10, verbose: bool=False):
    """
    Cracker method for Vigenere cipher. For each key length, message is split to multiple shorter messages, one for each
    key letter, and key letters are guessed using frequency analysis.
    :param stats: TextStats object of the text to be cracked
    :param dictionary: Dictionary constructed from the language of the plaintext
    :param n_best: Number of best plaintexts of each key length to save for further analysis
    :param key_limit: Maximal key length
    :param verbose: True to print some outputs, eg other candidates for plaintext
    :return: solved text, cipher name ("vigenere"), parameters: password
    """

    output_texts = []
    for key_len in range(2, key_limit):
        if verbose:
            print(key_len)
        # to simplify working with numpy, letters that don't fit in a table are thrown away
        filler_size = stats.N % key_len
        if filler_size:
            text = stats.text[0:-filler_size]
        else:
            text = stats.text

        # write the text into a matrix, each row is for one key letter
        m = int(len(text) / key_len)
        f = np.array(list(text))
        cipher_table = np.transpose(np.reshape(f, (m, key_len)))
        candidates = []

        for line_id in range(0, key_len):
            line_data = "".join(cipher_table[line_id, :])

            # try all possible shifts for the line (key letter) and save them
            line_candidates = []
            for shift in range(0, 26):
                shifted_line = rot(line_data, shift)
                shifted_score = compute_score(shifted_line, dictionary, bi=0, tri=0)
                line_candidates.append((shifted_score, shift, shifted_line))
            line_candidates.sort(key=lambda c: c[0], reverse=True)

            # only save the best guesses for each line
            candidates.append(line_candidates[0:n_best])

        possible_candidate_ids = list(range(0, n_best))
        output_texts_for_key_len = []

        # try all possible combinations of key letters in different lines, this will create the original key
        for combination in combinations(possible_candidate_ids, key_len):
            plaintext_table = np.zeros(cipher_table.shape)
            # convert the key to a readable format
            key = ""
            for line_id in range(0, key_len):
                key += chr(candidates[line_id][combination[line_id]][1] + 65)
                plaintext_table[line_id] = list(map(ord, list(candidates[line_id][combination[line_id]][2])))

            # assemble the lines together to read the main text
            table = np.reshape(np.transpose(plaintext_table), (1, len(text))).tolist()
            table = table[0]
            for i in range(0, len(table)):
                table[i] = chr(int(table[i]))
            text = "".join(table)

            score = compute_score(text, dictionary)
            output_texts_for_key_len.append((score, text, key, combination))

        output_texts_for_key_len.sort(key=lambda c: c[0], reverse=True)
        for i in range(0, n_best):
            if verbose:
                print(output_texts_for_key_len[i])
            output_texts.append(output_texts_for_key_len[i])

    # after all key sizes have been tried, select the best plaintext
    output_texts.sort(key=lambda c: c[0], reverse=True)
    return output_texts[0][1], "vigenere", output_texts[0][2]
