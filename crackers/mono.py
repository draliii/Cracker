from utils.text_analyzer import compute_score


def crack_mono(stats, dictionary):
    solutions = []

    # rot/ceasar
    for shift in range(1, 26):
        solution = rot(stats.text, shift)
        # print(solution)
        score = compute_score(solution, dictionary)
        solutions.append((score, solution, "rot"+str(shift)))

    # flip (A=Z, B=Y...)
    solution = flip_substitution(stats.text)
    score = compute_score(solution, dictionary)
    solutions.append((score, solution, "flip"))

    # affine ciphers
    for a, a_inv in zip([1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25],[1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17, 25]):
        for b in range(1, 26):
            solution = affine(stats.text, a_inv, b)
            score = compute_score(solution, dictionary)
            solutions.append((score, solution, "affine"+str(a)+","+str(b)))

    solutions.sort(key=lambda solution: solution[0], reverse=True)
    print(solutions[0][1])


def rot(cyphertext, shift):
    cleartext = ""
    for c in cyphertext:
        cl = shift_letter(c, shift)
        cleartext += cl
    return cleartext


def flip_substitution(cyphertext):
    cleartext = ""
    for c in cyphertext:
        letter_pos = ord(c) - 65
        letter_pos = abs(letter_pos - 25) + 65
        cleartext += chr(letter_pos)
    return cleartext


def affine(cyphertext, a_inv, b):
    cleartext = ""
    for c in cyphertext:
        cl = chr((a_inv*(ord(c)-65-b) % 26) + 65)
        cleartext += cl
    return cleartext


def shift_letter(c, shift):
    letter_pos = ord(c) - 65
    letter_pos = ((letter_pos + shift) % 26) + 65
    return chr(letter_pos)
