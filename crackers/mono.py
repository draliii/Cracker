from utils.dictionary import Dictionary
from utils.text_analyzer import compute_score, TextStats


def crack_mono(stats: TextStats, dictionary: Dictionary, final_round: bool=True, verbose: bool=False):
    """
    Method to crack the easiest monoalphabetic ciphers: ROT (Caesar's), Affine cipher, mirror flip. All ciphers with all
    parameters are generated, their outputs are compared to the given dictionary and sorted by likelihood. The best
    result is returned.
    :param stats: TextStats object of the text to be cracked
    :param dictionary: Dictionary constructed from the language of the plaintext
    :param final_round: True to use bigrams and trigrams when evaluated. In cases where eg. a transposition cipher is
     done after this substitution, it is better not to take bigrams and trigrams into account, and only use frequency
    :param verbose: True to print some outputs, eg other candidates for plaintext
    :return: solved text, cipher name ("rot", "affine", "flip"), parameters (shift, [a, a^(-1), b], _)
    """
    solutions = []

    # set coefficients to evaluate results
    if final_round:
        f = 1
        bi = 1
        tri = 1
    else:
        f = 1
        bi = 0
        tri = 0

    # try all possible rot/caesar shifts (0 is useless, so it is skipped)
    for shift in range(1, 26):
        solution = rot(stats.text, shift)
        score = compute_score(solution, dictionary, f, bi, tri)
        solutions.append((score, solution, "rot", shift))

    # try the flip cipher, it has no parameters so 0 is given instead
    solution = flip_substitution(stats.text)
    score = compute_score(solution, dictionary, f, bi, tri)
    solutions.append((score, solution, "flip", 0))

    # try affine ciphers
    # coefficients for a and inverse of a were computed beforehand, since it was faster
    for a, a_inv in zip([1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25], [1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17, 25]):
        # try all 25 shifts as before
        for b in range(1, 26):
            solution = affine(stats.text, a_inv, b)
            score = compute_score(solution, dictionary, f, bi, tri)
            solutions.append((score, solution, "affine", [a, a_inv, b]))

    # sort solutions by their score
    solutions.sort(key=lambda s: s[0], reverse=True)
    if verbose:
        for i in range(0, 10):
            print(solutions[i][0], solutions[i][2], solutions[i][3], solutions[i][1])

    # return only the best one
    return solutions[0][1], solutions[0][2], solutions[0][3]


def rot(ciphertext: str, shift: int):
    plaintext = ""
    for c in ciphertext:
        cl = shift_letter(c, -shift)
        plaintext += cl
    return plaintext


def flip_substitution(ciphertext: str):
    # A=Z, B=Y, C=X, D=W...
    plaintext = ""
    for c in ciphertext:
        letter_pos = ord(c) - 65
        letter_pos = abs(letter_pos - 25) + 65
        plaintext += chr(letter_pos)
    return plaintext


def affine(ciphertext: str, a_inv: int, b: int):
    plaintext = ""
    for c in ciphertext:
        cl = chr((a_inv*(ord(c)-65-b) % 26) + 65)
        plaintext += cl
    return plaintext


def shift_letter(c: str, shift: int):
    letter_pos = ord(c) - 65
    letter_pos = ((letter_pos + shift) % 26) + 65
    return chr(letter_pos)


def use_table(text: str, table: list):
    plaintext = ""
    for c in text:
        letter_pos = ord(c) - 65
        plaintext += chr(table[letter_pos] + 65)
    return plaintext
