import pickle as pkl
import heapq
import random

from crackers.mono import use_table
from utils.text_analyzer import TextStats, compute_score
from utils.dictionary import Dictionary
from utils.text_analyzer import compute_score_for_table
from copy import deepcopy


def brute_force(stats: TextStats, dictionary: Dictionary, f: int, bi: int, tri: int):
    stats_ids = sorted(range(len(stats.frequency)), key=stats.frequency.__getitem__)
    dict_ids = sorted(range(len(dictionary.frequency)), key=dictionary.frequency.__getitem__)

    # align frequently used letters together
    table = [-1] * 26
    for i in range(0, 26):
        table[stats_ids[i]] = dict_ids[i]

    plaintext = use_table(stats.text, table)
    score = compute_score(plaintext, dictionary, f, bi, tri)

    stable = 0
    while True:

        i = random.randint(0, 25)
        j = random.randint(0, 25)

        if i == j:
            continue

        new_table = table.copy()
        new_table[i] = table[j]
        new_table[j] = table[i]

        new_text = use_table(stats.text, new_table)
        new_score = compute_score(new_text, dictionary, f, bi, tri)

        if new_score > score:
            print(new_text, new_score)
            stable = 0
            table = new_table
            score = new_score
        else:
            stable += 1
            if stable > 1000000:
                break

    return new_text


def frequency(stats: TextStats, dictionary: Dictionary):
    swaps = []
    for i in range(0, 26):
        for j in range(i+1, 26):
            swaps.append((i, j))

    basic_table = make_basic_table(stats, dictionary)
    basic_score, basic_text = compute_score_for_table(basic_table, stats.text, dictionary, f=0, bi=0, tri=3)

    queue = []
    heapq.heappush(queue, (-basic_score, basic_table))
    visited_tables = []

    while len(queue) > 0:
        score, table = heapq.heappop(queue)
        score = -score
        print(score)
        if get_table_id(table) in visited_tables:
            continue
        visited_tables.append(get_table_id(table))
        for i, j in swaps:
            t = deepcopy(table)
            k = t[i]
            t[i] = t[j]
            t[j] = k
            s, text = compute_score_for_table(t, stats.text, dictionary, f=1, bi=0, tri=3)
            if s > score:
                heapq.heappush(queue,(-s, t))
                print(s, text)


def make_basic_table(stats: TextStats, dictionary: Dictionary):
    dict_letters = []
    text_letters = []
    for i in range(0, 26):
        dict_letters.append((i, dictionary.frequency[i]))
        text_letters.append((i, stats.frequency[i]))
    dict_letters.sort(key=lambda letter: letter[1], reverse=True)
    text_letters.sort(key=lambda letter: letter[1], reverse=True)

    table = [-1] * 26
    for i in range(0, 26):
        table[text_letters[i][0]] = dict_letters[i][0]
    return table


def get_table_id(table: list):
    table_id = 0
    for i in range(0, 26):
        table_id += table[i] * pow(26, i)
    return table_id


def demo():
    ciphertext = "RBLMRRMGELPQBMULQGMKLUFTGCMIJHMULTKBCQHCIURBMRQCRBLQMCURJHMPCIMWLPLAJCIARJFCVLCIRJWIILMPFJRQJSJRBLP" \
                 "BJTQLQCIMBJTQLWBLPLWLGMIOLQMSLQJHLRCHLFMRLPRBLKJFCGLRJFUMFFRBLHLHOLPQJSRBLSMHCFYRBMRRBLYBMUTIGJVLPL" \
                 "UHJPLKFJRQRBCQRCHLRJECUIMKACTFCMIMMIUFTGCMIJQQJIMFLQQMIUPJ"

    dictionary = pkl.load(open("/home/dita/ownCloud/Soutěže/Cracker/utils/en.pkl", "rb"))

    stats = TextStats(ciphertext)
    frequency(stats, dictionary)
    pass


if __name__ == "__main__":
    demo()
