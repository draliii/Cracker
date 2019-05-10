import numpy as np
from utils.text_analyzer import TextStats
from utils.text_analyzer import compute_score
from utils.dictionary import Dictionary
from itertools import permutations as permutations


def crack_transposition(stats: TextStats, dictionary: Dictionary, verbose: bool=False):
    """
    Method to crack table transpositions. It assumes that ciphertext was obtained by writing plaintext to rows of given
    size and then read by columns. If there are empty spaces in the table, they are filled by fake letters. This cracker
    identifies the correct plaintext by counting identical letters at it's end, and by comparing it to the dictionary.
    All possible table sizes are evaluated, as it doesn't take much time and size detection function that was used to
    get one table size can be confused if the filler uses random characters instead of all Xs.
    :param stats: TextStats object of the text to be cracked
    :param dictionary: Dictionary constructed from the language of the plaintext
    :param verbose: True to print some outputs, eg other candidates for plaintext
    :return: plaintext, cipher name ("transposition_table"), parameters (table height)
    """
    solutions = []

    # this doesn't work all that well, and it is found later on anyway
    #    likely_size = guess_table_size(stats)
    # if likely_size:
    #    solution = read_from_table(stats, likely_size)
    #    language_score = compute_score(solution, dictionary)
    #    solutions.append((language_score, solution, "guessed"+str(likely_size)))

    # try all possible table dimensions
    for size in range(2, stats.N):
        # table size must be divisible by the dimensions
        if not stats.N % size:
            solution = read_from_table(stats, size)
            # how many characters repeat at the end of the plaintext
            tail_score = count_tailing_letters(solution)
            language_score = compute_score(solution, dictionary)
            solutions.append((tail_score, language_score, solution, "transposition_table", [size]))

    # sort by language, but use tail_score for primary sorting
    solutions.sort(key=lambda s: s[1], reverse=True)
    solutions.sort(key=lambda s: s[0], reverse=True)

    if verbose:
        for i in range(0, len(solutions)):
            print(solutions[i][0], solutions[i][3], solutions[i][2])

    return solutions[0][2], solutions[0][3], solutions[0][4]


def read_from_table(stats: TextStats, table_width: int):
    # take the string from stats, feed it to an array and then read it along different axis to get plaintext
    m = int(stats.N/table_width)
    f = np.array(list(stats.text))
    cipher_table = np.transpose(np.reshape(f, (m, table_width)))
    table = np.reshape(cipher_table, (1, stats.N)).tolist()
    return "".join(table[0])


def crack_transposition_with_column_scrambling(stats: TextStats, dictionary: Dictionary, verbose: bool=False):
    """
    Method to crack table transpositions with column shuffling. The cipher is the same as table transposition above, but
    the columns are shuffled before message is read. The method will try all permutations of columns for tables with 7
    or less columns. Larger tables are skipped, because it would take ages to compute.
    :param stats: TextStats object of the text to be cracked
    :param dictionary: Dictionary constructed from the language of the plaintext
    :param verbose: True to print some outputs, eg other candidates for plaintext
    :return: plaintext, cipher name ("transposition_table_shuffled"), parameters: [table height, permutation]
    """
    solutions = []
    for size in range(2, stats.N):
        if not stats.N % size:
            n_cols = int(stats.N / size)
            if n_cols > 7:
                if verbose:
                    print("Can't guess with table size", size, "- too many column permutations, skipping")
                continue
            from math import factorial
            if verbose:
                print(n_cols, factorial(n_cols))

            # prepare a table to be shuffled
            cipher_table = generate_table(stats, size)
            # create permutations of [0, 1, ..., n_cols]
            for permutation in permutations(list(range(0, n_cols))):
                # apply permutation and read message
                shuffled_table = cipher_table[:, permutation]
                table = np.reshape(shuffled_table, (1, stats.N)).tolist()
                solution = "".join(table[0])
                language_score = compute_score(solution, dictionary)
                solutions.append((language_score, solution, size, permutation))

    solutions.sort(key=lambda s: s[0], reverse=True)
    if verbose:
        for i in range(0, min(len(solutions), 50)):
            print(solutions[i][0], solutions[i][1], solutions[i][2], solutions[i][3])

    return solutions[0][1], "transposition_table_shuffled", [solutions[0][2], solutions[0][3]]


def generate_table(stats: TextStats, table_width: int):
    m = int(stats.N/table_width)
    f = np.array(list(stats.text))
    cipher_table = np.transpose(np.reshape(f, (m, table_width)))
    return cipher_table


def guess_table_size(text: TextStats, filler: int="X"):
    """
    Finds how often filler characters appear. This can be used to detect table size, but turned out to be useless.
    :param text: ciphertext
    :param filler: character to work with
    :return: Likely table size
    """
    last_filler_pos = 0
    distances = {}
    best_size = -1
    best_size_value = -1
    for i in range(0, text.N):
        c = text.text[i]
        if c == filler:
            distance = i - last_filler_pos
            if distance not in distances:
                distances[distance] = 1
            else:
                distances[distance] += 1
            last_filler_pos = i
            if distances[distance] > best_size_value:
                best_size = distance
                best_size_value = distances[distance]

    if text.N % best_size:
        return False
    return best_size


def count_tailing_letters(text: str):
    if len(text) == 0:
        return 0
    last_char = text[-1]
    i = 1
    for i in range(1, len(text)):
        if text[-i] != last_char:
            break
    return i-1
