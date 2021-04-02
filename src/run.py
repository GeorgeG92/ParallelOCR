import sys
from arg_parser import arg_parser
from ocr import OCR
import logging


def main(args):
	OCR(args)
	return 0

if __name__ == "__main__":
	args = arg_parser(sys.argv)
	logging.basicConfig(level=getattr(logging, args.logging_level), 
		format="%(asctime)s|%(filename)-20.20s||%(funcName)-20.20s|%(levelname)-8.8s|%(message)s")
	main(args)
