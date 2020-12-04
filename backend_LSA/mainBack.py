import os
import sys
import shutil
import numpy as np
import scipy.spatial.distance
from zipfile import ZipFile
import matplotlib.pyplot as plt

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

	finalRes = np.zeros((numFiles,numFiles));

	with open(outpFile, 'w') as f:
		for i in range(numFiles):
			f.write(filenames[i]+",")
			print(filenames[i]+",")
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
	numDisp = min(5, numFiles*(numFiles-1)/2)
	maxInd = np.argpartition(finalRes, -numDisp)[-numDisp:]
	dicTop5 = dict((finalRes[elemPos] , (str(filenames[elemPos%numFiles]) + "\nand\n" + str(filenames[elemPos//numFiles]))) for elemPos in maxInd)
	top5Names = [key for key in sorted(dicTop5)]
	top5Coeffs = [dicTop5[key] for key in top5Names]
	
	plt.barh(range(len(dicTop5)), top5Names)
	plt.yticks(range(len(dicTop5)), top5Coeffs)
	plt.savefig(outpPng)
	
	
	try:
		shutil.rmtree('inputDir')
	except OSError as error:
		print("Directory does not exist.")
	