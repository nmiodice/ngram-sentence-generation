from nltk.util import ngrams
from util import Utilities
import re

class TextUtils:

	# Converts the file located at FILE_PATH to an ngram of with length N.
	# If the file does not exist, NONE is returned. Otherwise, an NGRAM is
	# returned. The type is NLTK.UTIL.NGRAMS
	@staticmethod
	def file_to_ngram(file_path, n):
		if n < 1:
			return None
		if Utilities.is_file(file_path) == False:
			return None
		fileContent = []
		file = Utilities.open_file(file_path);
		for line in file:
			fileContent += TextUtils.normalize_line(line)
			fileContent.append(' ')

		ng = ngrams(fileContent, n)
		return ng

	# Clean a line for use in creating an ngram. LINE is a string that will
	# be cleaned and returned to the caller. Cleaning process does:
	#	1. Remove non-alpha/whitespace characters, and replaces them with a
	#		space
	#	2. Converts to lower case
	#	3. Strips leading and trailing white space
	#	4. Removes duplicate white space
	# The returned value is a list, each element being one word from the
	# cleaned version of LINE, or order of original appearance 
	@staticmethod
	def normalize_line(line):
		line = line.lower()

		buffer = []
		for c in line:
			if c.isalpha() or c.isspace():
				buffer.append(c)
			else:
				buffer.append(' ')

		line = "".join(buffer)
		line = re.sub("\s+", " ", line)
		line = line.rstrip().lstrip()
		return line.split()
