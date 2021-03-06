import sys
import argparse
import os
import logging

logger = logging.getLogger(__file__)


def str2bool(v):
	if isinstance(v, bool):
	   return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')

def arg_parser(argv):
	"""Add command line arguments and parse user inputs.
	Args:
		argv: User input from the command line.
	Returns:
		An args object that contains parsed arguments.
	"""
	# Creating a parser
	parser = argparse.ArgumentParser(description='OCR')

	parser.add_argument('-l', '--logging', dest='logging_level', type=str.upper,
						choices=['debug', 'info', 'warning', 'error', 'critical'],
						default='info', help='set logging level')

	parser.add_argument('--docspath', dest='docsPath',
					default=os.path.join('..', 'documents'),
					help='Path to input documents')

	parser.add_argument('--imagespath', dest='imagesPath',
						default=os.path.join('..', 'images'),
						help='Path to image directory to be used for the pipelines')

	parser.add_argument('--exptype', type=str.lower, dest='expType',
						default='docx',
						help='Export in .csv or .docx format')

	parser.add_argument('--performance', dest='performance', type=int,
						default=2,
						help='Performance profiles: 0: light, 1:medium, 2:high',
						choices=[0, 1, 2])

	parser.add_argument('--cleanup', default=True, 
						help='Whether to clean up generated images after OCR')

	parser.add_argument('--dpi', type=int, default=300,
						help='Resolution of pdf2Image',
						choices=[150, 300, 600])

	parser.add_argument('--outputpath', dest='outputPath',
						default=os.path.join('..', 'output'),
						help='Path to generated csv with extracted text files')

	args = parser.parse_args(argv[1:])
	arg_checker(args)
	return args

def arg_checker(args):
	"""Processes arguments and performs validity checks for poppler and tesseract directories
	"""
	if not os.path.exists(args.imagesPath):
		logger.info('\tImage directory not found, creating...')
		#print('\tImage directory not found, creating...')
		os.mkdir(args.imagesPath)
	if not os.path.exists(args.outputPath):
		#print('\tOutput directory not found, creating...')
		logger.info('\tOutput directory not found, creating...')
		os.mkdir(args.outputPath)

