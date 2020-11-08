import os
import re

def walkThroughFiles(path, file_extensions):   
	"""
	Generator function: searches the directory recursively to obtain all files that match the file_extensions
	Args:
		path: input path to search in
		file_extensions: Tuple of extensions to filter on
	"""
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			if filename.endswith(file_extensions): 
				yield os.path.join(dirpath, filename).replace("\\","/")        # ensure right backslashes (Windows)!
				
def generateList(directory, file_extensions=('.pdf', '.tiff')):
	"""
	Populates a list of compatible files and returns it
	Args:
		directory: root directory of the documents
		file_extensions: Tuple of extensions to filter on
	Returns:
		A list of document paths
	"""
	documentsList = []                            
	for fname in walkThroughFiles(directory, file_extensions):
		documentsList.append(fname)
	return documentsList

def cleanText(text, exportType):
	"""
	Basic string cleaning function, removes non printable charactes as well as tabs and newlines
	Args:
		text: the text input
	Returns:
		The cleaned text
	"""
	if exportType=='csv':
		text = re.sub('[^Α-Ωa-zΈΌΊΏΉΎα-ω0-9A-Zάέόίώήύϊϋ\ \.,`#%&@:$·\-\*^/;()!\'/\"]', "", text)
	else:
		text = re.sub('[^Α-Ωa-zΈΌΊΏΉΎα-ω0-9A-Zάέόίώήύϊϋ\ \.\n,`#%&@:$·\-\*^/;()!\'/\"]', "", text)
	text = re.sub("(\ {2,})", " ", text)
	return text