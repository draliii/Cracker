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
    texts = ["TYOAK XMCLM LKDUT MCSDD MCXUB SDHMF CKFDK WKAXK UJLSW KJSUM BSXSD OKTTJ LSBMT AOSLS ULMYJ SDJMI KFAXK"
             "CLMFS KOLSD HMFJL SOKFJ STSBL MXS",

             "RBLMR RMGEL PQBMU LQGMK LUFTG CMIJH MULTK BCQHC IURBM RQCRB LQMCU RJHMC IMWLP LAJCI ARJFC VLCIR JWIIL"
             "MPFJR QJSJR BLPBJ TQLQC IMBJT QLWBL PLWLG MIOLQ MSLQJ HLRCH LFMRL PRBLK JFCGL RJFUM FFRBL HLHOL PQJSR"
             "BLSMH CFYRB MRRBL YBMUT IGJVL PLUHJ PLKFJ RQRBC QRCHL RJECU IMKAC TFCMI MMIUF TGCMI JQQJI MFLQQ MIUPJ",

             "ABCVT BAWHD AXJQG OENKR AUOIZ USRDY ENMHT TZAZX HUBLF VHFGR JIJTG FTSLV GUFDZ CNGWM QVUGU SZTAT BGMAJ"
             "YENEZ KHOOH ERIDY KSHFF WLMUX GMXKT UXMDT HNRQH DPVRQ BBMGF CBFDM CFEKM FMDYD VGODN AOFVO ZXSIX XRFWL"
             "SBNBP DMTUB GTTOA QASMG KOSUS ZTATB GOZSA OYWTU DYUPV WIWHT UXHTD BGUMC RIOEP HABPU Y",

             "ACRVN EHEHO AEHRO NNREX LUORI MSDTF FRREI ARESX ASCKA ODOSE RSTEY NDEYR SFIEL CBEPC NHAWF AUAVI LRWOT"
             "BANTI NNEVH EEVYS WIHDE LASRA IIIAA BNTEO EOEFN UTAIL AOLSS LDHRU",

             "GLIAX QKERP VYLIJ CIILW IPIRE JVSHV XIXSW MTMEV WMLRX RIXXJ ROXGI SSPRI IXGGE EQVRC GHVLL MXEEQ AEIWJ"
             "EMXIP VSEXM XMZWC WXOYW MREZI IYSLI WWRXX IRRRJ SXFXC LIXYI MEYAI MTIW",

             "GGJSS YWMYY MFMPF NFYVJ EJOYM VJNEM VMYQR ETVWY IWEKG KMRPE EXVGI YTKJV VFJFJ VYRVK YPYUW LJYPY JQRXV"
             "WEEXX EEMJE IEKMQ VGEXK XMRMI PLXFV VVXOM XJUTN WJELJ ENJAG VYAMI EWRTJ IGARV JEEEJ XVMOV LVQVA GWOJF"
             "GFSGW RYGVJ VX",

             "HHIEE TWSTF DETER SKKTO JNGZN UGXOJ UKSWH GHEST EUNES TUXMP QVQJS WZZLX QPVXR BFZFR APJFG YAVQR MLHEA"
             "NOOET WAGST NKKKJ IKCGY UKTCS NYDBA ITTNS TRNNH OEIBC LIQBN BQMBM QDEDB FGEIB ENAFL QPRBR HIHEI NONJO"
             "MAHMR XUTKV ZTSJG VUJNK RXLEF OIACF PERVE NDXLA WZMUW CIVMM TBEXG FEGFR NEARJ ECNNX"]

    dict_dir = "/home/dita/ownCloud/Soutěže/Cracker/utils/"
    dict_langs = ["cs", "en"]

    dicts = []
    for lang in dict_langs:
        d = pkl.load(open(dict_dir + lang + ".pkl", "rb"))
        dicts.append(d)

    for ciphertext in texts:
        stats = TextStats(ciphertext)

        identify_ciphers(stats, dicts[1])
