import sys
from argParser import argParser
from ocr import OCR

def main(args):
    OCR(args)
    return 0

if __name__ == "__main__":
    args = argParser(sys.argv)
    main(args)