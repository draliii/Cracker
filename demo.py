from crackers.mono import crack_mono
from crackers.transposition import crack_transposition_with_column_scrambling
from crackers.transposition import crack_transposition
from crackers.vigenere import crack_vigenere
from crackers.manual_substitution import solve_manually
from utils.dictionary import Dictionary
import pickle as pkl
from utils.text_analyzer import TextStats


def demo1(dictionary: Dictionary):
    ciphertext = "TYOAK XMCLM LKDUT MCSDD MCXUB SDHMF CKFDK WKAXK UJLSW KJSUM BSXSD OKTTJ LSBMT AOSLS ULMYJ SDJMI" \
                 "KFAXK CLMFS KOLSD HMFJL SOKFJ STSBL MXS"
    stats = TextStats(ciphertext)

    plaintext, method, parameters = crack_mono(stats, dictionary)
    return plaintext


def demo2(dictionary: Dictionary):
    ciphertext = "RBLMR RMGEL PQBMU LQGMK LUFTG CMIJH MULTK BCQHC IURBM RQCRB LQMCU RJHMC IMWLP LAJCI ARJFC VLCIR" \
                 "JWIIL MPFJR QJSJR BLPBJ TQLQC IMBJT QLWBL PLWLG MIOLQ MSLQJ HLRCH LFMRL PRBLK JFCGL RJFUM FFRBL" \
                 "HLHOL PQJSR BLSMH CFYRB MRRBL YBMUT IGJVL PLUHJ PLKFJ RQRBC QRCHL RJECU IMKAC TFCMI MMIUF TGCMI" \
                 "JQQJI MFLQQ MIUPJ"
    stats = TextStats(ciphertext)

    plaintext, method, parameters = solve_manually(stats, dictionary)
    return plaintext


def demo3(dictionary: Dictionary):
    ciphertext = "ABCVT BAWHD AXJQG OENKR AUOIZ USRDY ENMHT TZAZX HUBLF VHFGR JIJTG FTSLV GUFDZ CNGWM QVUGU SZTAT" \
                 "BGMAJ YENEZ KHOOH ERIDY KSHFF WLMUX GMXKT UXMDT HNRQH DPVRQ BBMGF CBFDM CFEKM FMDYD VGODN AOFVO" \
                 "ZXSIX XRFWL SBNBP DMTUB GTTOA QASMG KOSUS ZTATB GOZSA OYWTU DYUPV WIWHT UXHTD BGUMC RIOEP HABPU Y"
    stats = TextStats(ciphertext)

    plaintext = crack_vigenere(stats, dictionary)
    return plaintext


def demo4(dictionary: Dictionary):
    ciphertext = "ACRVN EHEHO AEHRO NNREX LUORI MSDTF FRREI ARESX ASCKA ODOSE RSTEY NDEYR SFIEL CBEPC NHAWF AUAVI" \
                 "LRWOT BANTI NNEVH EEVYS WIHDE LASRA IIIAA BNTEO EOEFN UTAIL AOLSS LDHRU"
    stats = TextStats(ciphertext)

    plaintext, method, parameters = crack_transposition_with_column_scrambling(stats, dictionary)
    return plaintext


def demo5(dictionary: Dictionary):
    ciphertext = "GLIAX QKERP VYLIJ CIILW IPIRE JVSHV XIXSW MTMEV WMLRX RIXXJ ROXGI SSPRI IXGGE EQVRC GHVLL MXEEQ" \
                 "AEIWJ EMXIP VSEXM XMZWC WXOYW MREZI IYSLI WWRXX IRRRJ SXFXC LIXYI MEYAI MTIW"
    stats = TextStats(ciphertext)

    scrambled_text, method, parameters = crack_mono(stats, dictionary, final_round=False)

    scrambled_stats = TextStats(scrambled_text)
    plaintext, method, parameters = crack_transposition(scrambled_stats, dictionary)
    return plaintext


def demo6(dictionary: Dictionary):
    ciphertext = "GGJSS YWMYY MFMPF NFYVJ EJOYM VJNEM VMYQR ETVWY IWEKG KMRPE EXVGI YTKJV VFJFJ VYRVK YPYUW LJYPY" \
                 "JQRXV WEEXX EEMJE IEKMQ VGEXK XMRMI PLXFV VVXOM XJUTN WJELJ ENJAG VYAMI EWRTJ IGARV JEEEJ XVMOV" \
                 "LVQVA GWOJF GFSGW RYGVJ VX"
    stats = TextStats(ciphertext)

    scrambled_text, method, parameters = crack_mono(stats, dictionary, final_round=False)

    scrambled_stats = TextStats(scrambled_text)
    plaintext, method, parameters = crack_transposition_with_column_scrambling(scrambled_stats, dictionary)
    return plaintext


def demo7(dictionary: Dictionary):
    ciphertext = "HHIEE TWSTF DETER SKKTO JNGZN UGXOJ UKSWH GHEST EUNES TUXMP QVQJS WZZLX QPVXR BFZFR APJFG YAVQR" \
                 "MLHEA NOOET WAGST NKKKJ IKCGY UKTCS NYDBA ITTNS TRNNH OEIBC LIQBN BQMBM QDEDB FGEIB ENAFL QPRBR" \
                 "HIHEI NONJO MAHMR XUTKV ZTSJG VUJNK RXLEF OIACF PERVE NDXLA WZMUW CIVMM TBEXG FEGFR NEARJ ECNNX"
    stats = TextStats(ciphertext)

    transposed_text, method, parameters = crack_transposition(stats, dictionary)
    transposed_stats = TextStats(transposed_text)

    plaintext, method, parameters = crack_vigenere(transposed_stats, dictionary, key_limit=7)
    return plaintext


def demo():
    dictionary = pkl.load(open("/home/dita/ownCloud/Soutěže/Cracker/utils/en.pkl", "rb"))
    print(demo1(dictionary))
    print(demo2(dictionary))
    print(demo3(dictionary))
    print(demo4(dictionary))
    print(demo5(dictionary))
    print(demo6(dictionary))
    print(demo7(dictionary))


if __name__ == "__main__":
    demo()
