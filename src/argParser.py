import sys
import argparse
import os

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
                        help='Path to Poppler "\bin\\pdftoppm.exe"')

    parser.add_argument('--imagespath', dest='imagesPath',
                        default=os.path.join('..', 'images'),
                        help='Path to image directory to be used for the pipelines')

    parser.add_argument('--performance', dest='performance',
                        default=2,
                        help='Performance profiles: 0: light, 1:medium, 2:high',
                        choices=[0, 1, 2])

    parser.add_argument('--cleanup',
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
                        help='Path to Tesseract executable"')

    args = parser.parse_args(argv[1:])
    argChecker(args)
    return args

def argChecker(args):
    """Processes arguments and performs validity checks
    Returns:
        Success Code
    """
    if not os.path.exists(args.imagesPath):
        print('\tImage directory not found, creating...')
        os.mkdir(args.imagesPath)
    if not os.path.exists(args.outputPath):
        print('\tOutput directory not found, creating...')
        os.mkdir(args.outputPath)

    #os.environ['popplerPath'] = os.path.join('..', 'poppler-0.68.0_x86', 'poppler-0.68.0', 'bin', 'pdftoppm.exe')
    os.environ['popplerPath'] = os.path.join('..', '..', '..', 'parallel ocr',
        'IBOR-Contract-Analysis','poppler-0.68.0_x86', 'poppler-0.68.0', 'bin', 'pdftoppm.exe')
    args.popplerPath = os.environ.get('popplerPath')

    if args.popplerPath is None:
        args.popplerPath = os.environ.get('popplerPath')
    assert os.path.exists(args.popplerPath), "Poppler extract not found at "+str(args.popplerPath)+", either provide a valid path on execution or add it to PATH"
    
    os.environ['tesseractPath'] = 'C://Program Files//Tesseract-OCR//tesseract.exe'
    args.tesseractPath = os.environ.get('tesseractPath')
    return 0

