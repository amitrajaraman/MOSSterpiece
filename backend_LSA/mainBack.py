import os
import sys
import shutil
import numpy as np
import scipy.spatial.distance
from zipfile import ZipFile

def cosine_similarity(c1, c2):
	if(c1.shape != c2.shape):
		print("ERROR"),
		return ""
	return (1 - scipy.spatial.distance.cosine(c1, c2))

if __name__ == "__main__":

	zipFilePath = ''
	try:
		zipFilePath = sys.argv[1]
	except:
		print("Usage: mainBack.py relative/path/to/filename.zip")
		print("Quitting")
		quit()
	with ZipFile(zipFilePath, 'r') as zipObj:
		zipObj.extractall('inputDir')
	directory = 'inputDir'
	outpFile = 'outpFile.csv'
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
		f = os.path.join(directory, filenames[i])
		f = open(f, "r")
		for line in f:
			for word in line.split():
				if(word not in baseDict.keys()):
					baseDict[word] = [0] * numFiles
				baseDict[word][i] += 1

	baseArray = np.array(list(baseDict.values()))
	#print(baseArray)

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
	lowRank = 1+int(np.cbrt(baseArray.shape[0]))
	# print(lowRank)
	if(lowRank > 300):
		lowRank = 300

	uRed = u[:lowRank, :lowRank]
	sRed = np.diag(s[:lowRank])
	
	arrRed = np.dot(np.dot(uRed, sRed), v)

	with open(outpFile, 'w') as f:
		for i in range(numFiles):
			f.write(filenames[i]+",")
		f.write("\n")
		for i in range(numFiles):
			for j in range(numFiles):
				f.write(str(cosine_similarity(arrRed[:, i], arrRed[:, j]))+","),
			f.write("\n")
	
	try:
		shutil.rmtree('inputDir')
	except OSError as error:
		print("Directory does not exist.")
	