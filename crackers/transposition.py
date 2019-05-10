import numpy as np
import pickle as pkl
from utils.text_analyzer import TextStats
from utils.text_analyzer import compute_score
from utils.dictionary import Dictionary


def crack_transposition(stats: TextStats, dictionary):
    solutions = []

    """
    likely_size = guess_table_size(stats)
    if likely_size:
        solution = read_from_table(stats, likely_size)
        language_score = compute_score(solution, dictionary)
        solutions.append((language_score, solution, "guessed"+str(likely_size)))
    """

    for size in range(2, stats.N):
        if not stats.N % size:
            solution = read_from_table(stats, size)
            tail_score = count_tailing_letters(solution)
            language_score = compute_score(solution, dictionary)
            solutions.append((tail_score, language_score, solution, "auto"+str(size)))

    solutions.sort(key=lambda solution: solution[0], reverse=True)
    for i in range(0, len(solutions)):
        print(solutions[i][0], solutions[i][3], solutions[i][2])


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


def count_tailing_letters(text: str):
    if len(text) == 0:
        return 0
    last_char = text[-1]
    i = 1
    for i in range(1, len(text)):
        if text[-i] != last_char:
            break
    return i-1


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
    ciphertexts = ["ABCVTBAWHDAXJQGOENKRAUOIZUSRDYENMHTTZAZXHUBLFVHFGRJIJTGFTSLVGUFDZCNGWMQVUGUSZTATBGMAJYENEZKHOOHERIDYKSHFF"
             "WLMUXGMXKTUXMDTHNRQHDPVRQBBMGFCBFDMCFEKMFMDYDVGODNAOFVOZXSIXXRFWLSBNBPDMTUBGTTOAQASMGKOSUSZTATBGOZSAOYWTU"
             "DYUPVWIWHTUXHTDBGUMCRIOEPHABPUY",
             "ACRVNEHEHOAEHRONNREXLUORIMSDTFFRREIARESXASCKAODOSERSTEYNDEYRSFIELCBEPCNHAWFAUAVILRWOTBANTINNEVHEEVYSWIHDE"
             "LASRAIIIAABNTEOEOEFNUTAILAOLSSLDHRU",
             "GLIAXQKERPVYLIJCIILWIPIREJVSHVXIXSWMTMEVWMLRXRIXXJROXGISSPRIIXGGEEQVRCGHVLLMXEEQAEIWJEMXIPVSEXMXMZWCWXOYW"
             "MREZIIYSLIWWRXXIRRRJSXFXCLIXYIMEYAIMTIW",
             "GGJSSYWMYYMFMPFNFYVJEJOYMVJNEMVMYQRETVWYIWEKGKMRPEEXVGIYTKJVVFJFJVYRVKYPYUWLJYPYJQRXVWEEXXEEMJEIEKMQVGEXK"
             "XMRMIPLXFVVVXOMXJUTNWJELJENJAGVYAMIEWRTJIGARVJEEEJXVMOVLVQVAGWOJFGFSGWRYGVJVX",
             "HHIEETWSTFDETERSKKTOJNGZNUGXOJUKSWHGHESTEUNESTUXMPQVQJSWZZLXQPVXRBFZFRAPJFGYAVQRMLHEANOOETWAGSTNKKKJIKCGY"
             "UKTCSNYDBAITTNSTRNNHOEIBCLIQBNBQMBMQDEDBFGEIBENAFLQPRBRHIHEINONJOMAHMRXUTKVZTSJGVUJNKRXLEFOIACFPERVENDXLA"
             "WZMUWCIVMMTBEXGFEGFRNEARJECNNX"]

    dict = pkl.load(open("/home/dita/ownCloud/Soutěže/Cracker/utils/en.pkl", "rb"))

    for t in ciphertexts:
        print()
        print(t)
        stats = TextStats(t)
        crack_transposition(stats, dict)

