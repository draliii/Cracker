import numpy as np


class TextStats():
    def __init__(self, text):
        self.text = text.replace(" ", "")
        self.N = len(self.text)
        self.ic = None
        self.histogram = None
        self.frequency = None

    def compute_histogram(self):
        self.histogram = [0]*26
        for t in self.text:
            self.histogram[ord(t)-65] += 1

    def compute_frequency(self):
        self.frequency = np.divide(self.histogram, self.N)

    def coincidence_index(self):
        self.ic = 26*(np.sum(np.multiply(self.histogram, np.subtract(self.histogram, 1)))/(self.N * (self.N -1)))

    def compute_stats(self):
        self.compute_histogram()
        self.compute_frequency()
        self.coincidence_index()


if __name__ == "__main__":
    # texts = "FUBSWRJUDSKLF NHBV DUH DQDORJRXV WR WKH KRXVH DQG FDU NHBV ZH FDUUB LQ RXU GDLOB OLYHV DQG VHUYH D VLPLODU SXUSRVH",\
    #         "VEH IYCFBYSYJO DEHCQB CUIIQWU JUNJ IXQBB RU SQBBUT FBQYD JUNJ QDT JXU UDSHOFJUT VEHC SYFXUH JUNJ",\
    #         "ZFA KAQG ZI VA SGAH CNA IVZCYPAH TNIW C KAQ GISNOA EFYOF GADAOZG ZFAW BANFCBG NCPHIWDQ TNIW ZFA DCNMA GAZ IT CDD SGCVDA KAQG",\
    #         "GLNTA JGZIB XQXQR BKQSQ GLKMQ RCMPK QMCZP XNRMD PSNFX SNGBZ BMCGL CMPKS RGMLZ SJJBE SIBXG QTQBE RMRPS LQCMP KKBQQ SDBGL RMZPX NRGZC MPK"
    #
    # for text in texts:
    #     text = text.replace(" ", "")
    #     stats = TextStats(text)
    #     stats.compute_stats()
    #
    #     print(stats.ic)

    f = open("/home/dita/ownCloud/Soutěže/Cracker/utils/en-robin-hood.txt")
    line = f.readline()
    line = line.replace(" ", "")
    line = line[0:len(line)-1]
    stats = TextStats(line)
    stats.compute_stats()
    print(stats.ic)


    text = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSPMYKVQXJTDCIOMEEXDQVSRXLRLKZHOV"
    stats = TextStats(text)
    stats.compute_stats()
    print(stats.ic)

