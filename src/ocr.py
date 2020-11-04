import os
import subprocess
from shutil import copyfile, rmtree
import multiprocessing as mp
import pytesseract as ps
from misc import walkThroughFiles, generateList, cleanText
import pandas as pd
try:
	from PIL import Image
except ImportError:
	import Image

class OCR():
	def __init__(self, args):
		self.docsPath = args.docsPath
		self.popplerPath = args.popplerPath
		self.imagesPath = args.imagesPath
		self.performance = args.performance
		self.cleanup = args.cleanup
		self.outputPath = args.outputPath
		self.tesseractPath = args.tesseractPath
		self.dpi = args.dpi

		self.docList = generateList(self.docsPath)
		if self.performance==2:
			self.concurrent = min(len(self.docList),mp.cpu_count())
		elif self.performance==1:
			self.concurrent = min(len(self.docList),int(mp.cpu_count()/2))
		else:
			self.concurrent = min(len(self.docList), int(mp.cpu_count()/4))
		self.runOCR()


	def ocr(self, imagePath): 
		"""
		Performs OCR on an image using Tesseract
		Args:
			imagePath: the path to the image to perform OCR on
		"""
		image = Image.open(imagePath)
		ps.pytesseract.tesseract_cmd = self.tesseractPath
		text = ps.image_to_string(image)
		#text = text.translate(str.maketrans('', '', string.punctuation)).lower().rstrip()    
		return text


	def ocrPipeline(self, docPath):
		"""
		OCR Pipeline that transforms a document to one images/page and then extracts the text from it
			Runs in multiprocessing
		Args:
			docPath: the path to the input document
		"""
		# pdf to Images
		print("\tProcessing document: "+str(docPath))
		head, tail = os.path.split(docPath)             # head='./../../', tail='bla.ext'
		fileName, ext = os.path.splitext(tail)
		imagePath = os.path.join(self.imagesPath, fileName)
		if not os.path.exists(imagePath):
			os.mkdir(imagePath)
		if docPath.lower().endswith(".pdf"):
			outputfile = os.path.join(imagePath, fileName)
			process = subprocess.Popen('"%s" -jpeg -r %s "%s" "%s"' % (self.popplerPath, self.dpi, docPath, outputfile))
			out, err = process.communicate()
		else:
			copyfile(docPath, os.path.join(imagePath, tail))
		# Images to Text
		imagesList =  generateList(imagePath, file_extensions=('.jpg', '.tiff'))
		finalText = ' '.join([self.ocr(imagePath) for imagePath in imagesList])
		finalText = cleanText(finalText)
		returnTuple = (tail, docPath, finalText)

		if self.cleanup:
			rmtree(imagePath)
		return returnTuple


	def exportResults(self, textList):
		"""
		Persists the extracted text to disk in .csv format
		Args:
			textList: A list of tuples containing document content and metadata
		"""
		print("Exporting results in "+str(self.outputPath))
		df = pd.DataFrame(textList, columns=['document', 'path', 'text'])
		df.to_csv(os.path.join(self.outputPath, 'results.csv'), index=False)


	def runOCR(self):
		"""
		Function that sets the OCR pipeline in motion
		"""
		print("Running OCR on "+str(len(self.docList))+" documents using "+str(self.concurrent)+" processes")
		p=mp.Pool(processes = self.concurrent)  
		textList = p.starmap(self.ocrPipeline, zip(self.docList))
		p.close()
		p.join()
		self.exportResults(textList)