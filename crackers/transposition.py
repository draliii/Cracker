import numpy as np
import pickle as pkl
from utils.text_analyzer import TextStats
from utils.text_analyzer import compute_score
from utils.dictionary import Dictionary


def crack_transposition(stats: TextStats, dictionary):
    solutions = []

    likely_size = guess_table_size(stats)
    if likely_size:
        solution = read_from_table(stats, likely_size)
        score = compute_score(solution, dictionary)
        solutions.append((score, solution, "guessed"+str(likely_size)))

    for size in range(2, stats.N):
        if not stats.N % size:
            solution = read_from_table(stats, size)
            score = compute_score(solution, dictionary)
            solutions.append((score, solution, "auto"+str(size)))

    solutions.sort(key=lambda solution: solution[0], reverse=True)
    for i in range(0, 10):
        print(solutions[i][2], solutions[i][1])


def guess_table_size(text: TextStats, filler:int="X"):
    """
    Finds how often filler characters appear. This can be used to detect table size
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


def read_from_table(stats: TextStats, table_width):
    m = int(stats.N/table_width)
    f = np.array(list(stats.text))
    cipher_table = np.transpose(np.reshape(f, (m, table_width)))
    # print(cipher_table)
    table = np.reshape(cipher_table, (1, stats.N)).tolist()
    return "".join(table[0])


if __name__ == "__main__":
    ciphertext = "HHIEETWSTFDETERSKKTOJNGZNUGXOJUKSWHGHESTEUNESTUXMPQVQJSWZZLXQPVXRBFZFRAPJFGYAVQRMLHEANOOETWAGSTNKKK" \
                 "JIKCGYUKTCSNYDBAITTNSTRNNHOEIBCLIQBNBQMBMQDEDBFGEIBENAFLQPRBRHIHEINONJOMAHMRXUTKVZTSJGVUJNKRXLEFOIA" \
                 "CFPERVENDXLAWZMUWCIVMMTBEXGFEGFRNEARJECNNX"
    ciphertext = "GLIAXQKERPVYLIJCIILWIPIREJVSHVXIXSWMTMEVWMLRXRIXXJROXGISSPRIIXGGEEQVRCGHVLLMXEEQAEIWJEMXIPVSEXMXMZW" \
                 "CWXOYWMREZIIYSLIWWRXXIRRRJSXFXCLIXYIMEYAIMTIW"

    dict = pkl.load(open("/home/dita/ownCloud/Soutěže/Cracker/utils/en.pkl", "rb"))

    stats = TextStats(ciphertext)
    crack_transposition(stats, dict)
