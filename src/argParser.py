import sys
import argparse
import os

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def argParser(argv):
    """Add command line arguments and parse user inputs.
    Args:
        argv: User input from the command line.
    Returns:
        An args object that contains parsed arguments.
    """
    # Creating a parser
    parser = argparse.ArgumentParser(description='OCR')

    parser.add_argument('--docspath', dest='docsPath',
                    default=os.path.join('..', 'documents'),
                    help='Path to input documents')

    parser.add_argument('--popplerpath', dest='popplerPath',
                        default=None,
                        help='Path to Poppler pdftoppm.exe')

    parser.add_argument('--imagespath', dest='imagesPath',
                        default=os.path.join('..', 'images'),
                        help='Path to image directory to be used for the pipelines')

    parser.add_argument('--performance', dest='performance',
                        default=2,
                        help='Performance profiles: 0: light, 1:medium, 2:high',
                        choices=[0, 1, 2])

    parser.add_argument('--cleanup', type=str2bool,
                        default=True,
                        help='Whether to clean up generated images after OCR',
                        choices=[True, False])

    parser.add_argument('--dpi',
                        default=300,
                        help='Resolution of pdf2Image',
                        choices=[150, 300, 600])

    parser.add_argument('--outputpath', dest='outputPath',
                        default=os.path.join('..', 'output'),
                        help='Path to generated csv with extracted text files')

    parser.add_argument('--tesseractpath', dest='tesseractPath',
                        default=None,
                        help='Path to tesseract.exe"')

    args = parser.parse_args(argv[1:])
    argChecker(args)
    return args

def argChecker(args):
    """Processes arguments and performs validity checks for poppler and tesseract directories
    Returns:
        Success Code
    """
    if not os.path.exists(args.imagesPath):
        print('\tImage directory not found, creating...')
        os.mkdir(args.imagesPath)
    if not os.path.exists(args.outputPath):
        print('\tOutput directory not found, creating...')
        os.mkdir(args.outputPath)

    if args.popplerPath is None:
        args.popplerPath = os.path.join(os.environ.get('popplerPath'), 'pdftoppm.exe')
    assert os.path.exists(args.popplerPath), "Poppler extract not found at "+str(args.popplerPath)+", either provide a valid path on execution or add it to PATH"
    
    args.tesseractPath = os.path.join(os.environ.get('tesseractPath'), 'tesseract.exe')
    assert os.path.exists(args.tesseractPath), "tesseract.exe extract not found at "+str(args.tesseractPath)+", please add it to 'tesseractPath' environmental variable"
    return 0

