import os
import sys
import shutil
import re
import numpy as np
import scipy.spatial.distance
from zipfile import ZipFile
import matplotlib.pyplot as plt

def do_file(fname):
    """ Run on just one file.
    """
    source = open(fname)
    mod = open(fname + ",strip", "w")

    prev_toktype = token.INDENT
    first_line = None
    last_lineno = -1
    last_col = 0

    tokgen = tokenize.generate_tokens(source.readline)
    for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
        if 0:   # Change to if 1 to see the tokens fly by.
            print("%10s %-14s %-20r %r" % (
                tokenize.tok_name.get(toktype, toktype),
                "%d.%d-%d.%d" % (slineno, scol, elineno, ecol),
                ttext, ltext
                ))
        if slineno > last_lineno:
            last_col = 0
        if scol > last_col:
            mod.write(" " * (scol - last_col))
        if toktype == token.STRING and prev_toktype == token.INDENT:
            # Docstring
            mod.write("#--")
        elif toktype == tokenize.COMMENT:
            # Comment
            mod.write("##\n")
        else:
            mod.write(ttext)
        prev_toktype = toktype
        last_col = ecol
        last_lineno = elineno

def comment_remover_cpp(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def cosine_similarity(c1, c2):
	if(c1.shape != c2.shape):
		print("ERROR"),
		return ""
	return (1 - scipy.spatial.distance.cosine(c1, c2))

if __name__ == "__main__":

	# Location of the (temporary) directory the zip file is unzipped to
	directory = 'inputDir'
	# Location of the output CSV file
	outpFile = 'outpFile.csv'
	# Location of the output image barh graph
	outpPng = 'outpImg.png'
	# n such that top n results are displayed in the bar graph
	barGraphParam = 5


	zipFilePath = ''
	try:
		zipFilePath = sys.argv[1]
	except:
		print("Usage: mainBack.py relative/path/to/filename.zip")
		print("Quitting")
		quit()
	with ZipFile(zipFilePath, 'r') as zipObj:
		zipObj.extractall('inputDir')
	filenames = [name for name in os.listdir(directory)]
	numFiles = len(filenames)
	baseDict = {}	

	"""
	Have to preprocess files
	* Remove things with only numeric characters
	* Remove syntactic tokens like ; for C++
	* Remove comments
	"""
	for i in range(numFiles):
		tempF = os.path.join(directory, filenames[i])
		fileExt = (os.path.splitext(tempF))[1]
		if(fileExt == '.py'):
			do_file(tempF)
		with open(tempF,'r') as readF:
			f = readF.read()
			# print(f)
			# print()
			if(fileExt == '.cpp'):
				f = comment_remover_cpp(f)
			f = f.replace('\n', '').replace('\r', '').replace('\t', '')
			re.sub(' +',' ',f)
			# print(f)
			# print(f)
			for word in f.split():
				if(word not in baseDict.keys()):
					baseDict[word] = [0] * numFiles
				baseDict[word][i] += 1

	baseArray = np.array(list(baseDict.values()))
	# print(baseArray)

	#Do some weighting to the matrix
	"""
	Term-weighting algorithms are then applied to matrix A.
	The purpose of applying weighting algorithms is to increase or decrease
	the importance of terms using local and global weights in order to improve
	detection performance.
	With document length normalization the term values are adjusted 
	depending on the length of each file in the corpus.

	* Term-frequency local weighting
	* Normal global weighting
	* Cosine normalization
	"""

	# print(baseArray.shape)

	u, s, v = np.linalg.svd(baseArray, False)
	# print(baseArray.shape[0])
	lowRank = 1+int(np.sqrt(baseArray.shape[0]))
	
	if (lowRank < numFiles):
		lowRank = numFiles+1


	# print(lowRank)
	if(lowRank > 300):
		lowRank = 300

	uRed = u[:lowRank, :]
	sRed = np.diag(s[:lowRank])

	# print(baseArray.shape)
	# print(lowRank)

	# print(uRed.shape)
	# print(sRed.shape)
	# print(v.shape)
	
	arrRed = np.dot(np.dot(uRed, sRed), v)

	finalRes = np.zeros((numFiles,numFiles));

	with open("../src/assets/results/outpFile.csv", 'w') as f:
		for i in range(numFiles):
			f.write(filenames[i]+",")
			# print(filenames[i]+",")
		f.write("\n")
		for i in range(numFiles):
			finalRes[i,i] = 1.0
			for j in range(numFiles):
				if(i < j):
					finalRes[i,j] = str(cosine_similarity(arrRed[:, i], arrRed[:, j]))
					# finalRes[j,i] = finalRes[i,j]
				f.write(str(finalRes[min(i,j),max(i,j)]) + ",")
			f.write("\n")
	

	for i in range(numFiles):
		finalRes[i,i] = 0

	finalRes = np.reshape(finalRes, (numFiles*numFiles))
	numDisp = int(min(barGraphParam, numFiles*(numFiles-1)/2))
	maxInd = [0 for x in range(numDisp)]
	dicTop5 = {}
	# for x in filenames:
	# 	print(x)
	# print("Size is "+str(numFiles))
	for pos in range(numDisp):
		dicTop5[finalRes[np.argmax(finalRes)]] = str(filenames[np.argmax(finalRes) % numFiles]) + " and\n" + str(filenames[np.argmax(finalRes) // numFiles])
		# dicTop5[finalRes[np.argmax(finalRes)]] = str(np.argmax(finalRes) % numFiles) + " and\n" + str(np.argmax(finalRes) // numFiles)
		# print(np.argmax(finalRes), finalRes[np.argmax(finalRes)], dicTop5[finalRes[np.argmax(finalRes)]])
		finalRes[np.argmax(finalRes)] = 0
	# print(dicTop5)
	# for key in dicTop5:
	# 	print(key, dicTop5[key])
	top5Names = [key for key in sorted(dicTop5)]
	top5Coeffs = [dicTop5[key] for key in top5Names]
	
	fig, ax = plt.subplots()
	ax.barh(range(len(dicTop5)), top5Names)
	plt.yticks(range(len(dicTop5)), top5Coeffs)

	for index, value in enumerate(top5Names):
	    plt.text(value, index, str(round(value,3)))
	right_side = ax.spines["right"]
	right_side.set_visible(False)

	plt.tight_layout()
	plt.savefig("../src/assets/results/outpImg.png")
	
	
	try:
		shutil.rmtree('inputDir')
	except OSError as error:
		print("Directory does not exist.")