import pickle as pkl
from utils.text_analyzer import TextStats
from crackers.mono import crack_mono
from utils.dictionary import Dictionary


def identify_ciphers(stats, dictionary):
    print("IC of ciphertext is " + str(stats.ic) + " , IC of dictionary is " + str(dictionary.ic))
    if (abs(stats.ic - dictionary.ic)) < 0.4:
        print("Monoalphabetic substitution was likely used")
        crack_mono(stats, dictionary)
    else:
        print("Monoalphabetic substitution was not used")


if __name__ == "__main__":
    texts = ["FUBSWRJUDSKLF NHBV DUH DQDORJRXV WR WKH KRXVH DQG FDU NHBV ZH FDUUB LQ RXU GDLOB OLYHV DQG VHUYH D VLPLODU SXUSRVH",
             "VEH IYCFBYSYJO DEHCQB CUIIQWU JUNJ IXQBB RU SQBBUT FBQYD JUNJ QDT JXU UDSHOFJUT VEHC SYFXUH JUNJ",
             "ZFA KAQG ZI VA SGAH CNA IVZCYPAH TNIW C KAQ GISNOA EFYOF GADAOZG ZFAW BANFCBG NCPHIWDQ TNIW ZFA DCNMA GAZ IT CDD SGCVDA KAQG",
             "GLNTA JGZIB XQXQR BKQSQ GLKMQ RCMPK QMCZP XNRMD PSNFX SNGBZ BMCGL CMPKS RGMLZ SJJBE SIBXG QTQBE RMRPS LQCMP KKBQQ SDBGL RMZPX NRGZC MPK"]
    ciphertext = texts[1]
    dict_dir = "/home/dita/ownCloud/Soutěže/Cracker/utils/"
    dict_langs = ["cs", "en"]

    dicts = []
    for lang in dict_langs:
        d = pkl.load(open(dict_dir + lang + ".pkl", "rb"))
        dicts.append(d)

    stats = TextStats(ciphertext)

    identify_ciphers(stats, dicts[1])