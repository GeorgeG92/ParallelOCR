import os
import subprocess
from shutil import copyfile, rmtree
import multiprocessing as mp
import pytesseract as ps
from misc import walk_through_files, generate_list, clean_text
import pandas as pd
try:
	from PIL import Image
except ImportError:
	import Image
import PyPDF2
import docx
import logging

logger = logging.getLogger(__file__)


class OCR():
	def __init__(self, args):
		self.docsPath = args.docsPath
		self.imagesPath = args.imagesPath
		self.performance = args.performance
		self.cleanup = args.cleanup
		self.outputPath = args.outputPath
		self.expType = args.expType
		self.dpi = args.dpi

		self.docList = generate_list(self.docsPath)
		if self.performance==2:
			self.concurrent = min(len(self.docList),mp.cpu_count())
		elif self.performance==1:
			self.concurrent = min(len(self.docList),int(mp.cpu_count()/2))
		else:
			self.concurrent = min(len(self.docList), int(mp.cpu_count()/4))
		self.run_OCR()


	def ocr(self, imagePath): 
		"""
		Performs OCR on an image using Tesseract
		Args:
			imagePath: the path to the image to perform OCR on
		"""
		image = Image.open(imagePath)
		#ps.pytesseract.tesseract_cmd = self.tesseractPath
		text = ps.image_to_string(image)
		#text = text.translate(str.maketrans('', '', string.punctuation)).lower().rstrip()    
		return text

	def test_pdf_readable(self, docPath):
		"""
		Tests whether a pdf is readable using the pypdf library
		Returns a boolean value
		"""
		reader = PyPDF2.PdfFileReader(docPath)
		pdftext = ''
		for page in range(reader.getNumPages()):
		    pagetext = reader.getPage(page).extractText()
		    pdftext += pagetext
		return len(pdftext)>0, pdftext

	def ocr_pipeline(self, docPath):
		"""
		OCR Pipeline that transforms a document to one image/page and then extracts the text from it
			Runs in multiprocessing
		Args:
			docPath: the path to the input document
		"""
		# pdf to Images
		logger.info("\tProcessing document: {docPath}".format(docPath=docPath))
		head, tail = os.path.split(docPath)                   # head='./../../', tail='bla.ext'
		readable, finalText = self.test_pdf_readable(docPath)
		if not readable:                                      # OCR
			fileName, ext = os.path.splitext(tail)
			imagePath = os.path.join(self.imagesPath, fileName)
			if not os.path.exists(imagePath):
				os.mkdir(imagePath)
			if docPath.lower().endswith(".pdf"):
				outputfile = os.path.join(imagePath, fileName)
				cp = subprocess.run('pdftoppm -jpeg -r {dpi} {path} {out}'.format(dpi=self.dpi, path=docPath, out=outputfile).split())
			else:
				copyfile(docPath, os.path.join(imagePath, tail))
			# Images to Text
			imagesList =  generate_list(imagePath, file_extensions=('.jpg', '.tiff'))
			finalText = ' '.join([self.ocr(imagePath) for imagePath in imagesList])
			if self.cleanup:
				rmtree(imagePath)
		finalText = clean_text(finalText, self.expType)
		returnTuple = (tail, docPath, finalText)
		return returnTuple


	def export_results(self, textList):
		"""
		Persists the extracted text to disk in .docx or .csv format
		Args:
			textList: A list of tuples containing document content and metadata
		"""
		if self.expType=='docx':
			logger.info("Exporting documents in .docx format: {outpath}".format(outpath=self.outputPath))
			for docList in textList:
				docPath = os.path.join(self.outputPath, ''.join(docList[0].split('.')[:-1])+'.docx')
				docxDoc = docx.Document()
				for paragraph in docList[2].split('\n'):
					docxDoc.add_paragraph(paragraph)
				docxDoc.save(docPath)
		else:
			logger.info("Exporting documents in .csv format: {outpath}".format(outpath=self.outputPath))
			df = pd.DataFrame(textList, columns=['document', 'path', 'text'])
			df.to_csv(os.path.join(self.outputPath, 'results.csv'), index=False)
			logger.info("Done")

	def run_OCR(self):
		"""
		Function that sets the OCR pipeline in motion
		"""
		logger.info("Extracting text from {d} documents using {c} processes".format(d=len(self.docList), c=self.concurrent))
		p=mp.Pool(processes = self.concurrent)  
		textList = p.starmap(self.ocr_pipeline, zip(self.docList))
		p.close()
		p.join()
		self.export_results(textList)