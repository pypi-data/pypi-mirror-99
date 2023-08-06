import codecs
from chardet import detect
from subsparser.constants import Extensions
from subsparser.readers.srt import SRTReader
from subsparser.readers.txt import TXTReader


class Subtitle:

    def __init__(self, path, encoding='utf-8', language_code=None):
        self.path = path
        self.language_code = None
        self.ext = Extensions.get(path)
        self.encoding = encoding
        self.size = None
        self.contents = None
        self.style = None
        self.data = None


    def detect_encoding(self):
        with open(file=self.path, mode='rb') as f:
            info = detect(f.read())
        self.encoding = info and info['encoding'] or self.encoding
        return self


    def read(self):
        with open(file=self.path, encoding=self.encoding, mode="r") as f:
            self.contents = f.readlines()
        return self

    def parse(self):
        if (self.ext == Extensions.SRT.value) or \
            (self.ext == Extensions.WEBVTT.value) or \
                (self.ext == Extensions.WEBVTT.value):
            self.data = SRTReader.parse(self.contents)
        elif self.ext == Extensions.TXT.value:
            self.data = TXTReader.parse(self.contents)
        return self.data

    def print(self):
        print("Path: %s" % (self.path))
        print("Encoding: %s" % (self.encoding))
        print("DATA: ")
        for ins in self.data:
            print(ins.start, ins.end, ins.text)