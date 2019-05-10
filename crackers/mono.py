from utils.text_analyzer import compute_score
import random


def crack_mono(stats, dictionary, final_round=True, verbose=False):
    solutions = []
    if final_round:
        f = 1
        bi = 1
        tri = 1
    else:
        f = 1
        bi = 0
        tri = 0

    # rot/caesar
    for shift in range(1, 26):
        solution = rot(stats.text, shift)
        # print(solution)
        score = compute_score(solution, dictionary, f, bi, tri)
        solutions.append((score, solution, "rot"+str(shift)))

    # flip (A=Z, B=Y...)
    solution = flip_substitution(stats.text)
    score = compute_score(solution, dictionary, f, bi, tri)
    solutions.append((score, solution, "flip"))

    # affine ciphers
    for a, a_inv in zip([1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25],[1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17, 25]):
        for b in range(1, 26):
            solution = affine(stats.text, a_inv, b)
            score = compute_score(solution, dictionary, f, bi, tri)
            solutions.append((score, solution, "affine"+str(a)+","+str(b)))

    solutions.sort(key=lambda solution: solution[0], reverse=True)
    if verbose:
        for i in range(0, 10):
            print(solutions[i][0], solutions[i][2], solutions[i][1])

    return solutions[0][1]


def rot(ciphertext, shift):
    plaintext = ""
    for c in ciphertext:
        cl = shift_letter(c, shift)
        plaintext += cl
    return plaintext


def flip_substitution(cyphertext):
    plaintext = ""
    for c in cyphertext:
        letter_pos = ord(c) - 65
        letter_pos = abs(letter_pos - 25) + 65
        plaintext += chr(letter_pos)
    return plaintext


def affine(ciphertext, a_inv, b):
    plaintext = ""
    for c in ciphertext:
        cl = chr((a_inv*(ord(c)-65-b) % 26) + 65)
        plaintext += cl
    return plaintext


def shift_letter(c, shift):
    letter_pos = ord(c) - 65
    letter_pos = ((letter_pos + shift) % 26) + 65
    return chr(letter_pos)


def brute_force(stats, dictionary, f, bi, tri):
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


def use_table(text, table):
    plaintext = ""
    for c in text:
        letter_pos = ord(c) - 65
        plaintext += chr(table[letter_pos] + 65)
    return plaintext

