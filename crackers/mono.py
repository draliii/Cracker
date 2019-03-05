from utils.text_analyzer import compute_score


def crack_mono(stats, dictionary):
    solutions = []

    # rot/ceasar
    for shift in range(1, 26):
        solution = rot(stats.text, shift)
        # print(solution)
        score = compute_score(solution, dictionary)
        solutions.append((score, solution))

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


def shift_letter(c, shift):
    letter_pos = ord(c) - 65
    letter_pos = ((letter_pos + shift) % 26) + 65
    return chr(letter_pos)
