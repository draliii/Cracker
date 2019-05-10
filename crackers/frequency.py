import matplotlib.pyplot as plt
import pickle as pkl
from utils.text_analyzer import TextStats
from utils.dictionary import Dictionary


def frequency(stats: TextStats, dictionary: Dictionary):
    pass


def demo():
    ciphertext = "RBLMRRMGELPQBMULQGMKLUFTGCMIJHMULTKBCQHCIURBMRQCRBLQMCURJHMPCIMWLPLAJCIARJFCVLCIRJWIILMPFJRQJSJRBLP" \
                 "BJTQLQCIMBJTQLWBLPLWLGMIOLQMSLQJHLRCHLFMRLPRBLKJFCGLRJFUMFFRBLHLHOLPQJSRBLSMHCFYRBMRRBLYBMUTIGJVLPL" \
                 "UHJPLKFJRQRBCQRCHLRJECUIMKACTFCMIMMIUFTGCMIJQQJIMFLQQMIUPJ"
    dictionary = pkl.load(open("/home/dita/ownCloud/Soutěže/Cracker/utils/en.pkl", "rb"))

    stats = TextStats(ciphertext)
    pass


if __name__ == "__main__":
    demo()
