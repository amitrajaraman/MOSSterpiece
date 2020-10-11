import os
import numpy as np
import scipy.spatial.distance

def cosine_similarity(c1, c2):
	if(c1.shape != c2.shape):
		print("ERROR")
		return 0
	return (1 - scipy.spatial.distance.cosine(c1, c2))

if __name__ == "__main__":
	directory = 'inputDir'
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
	baseArray = baseArray.T
	
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

	u, s, v = np.linalg.svd(baseArray, False)
	
	lowRank = 20
	# Pick optimal rank reduction; google!!!

	uRed = u[:, :lowRank]
	sRed = np.diag(s[:lowRank])
	vRed = v[:, :lowRank]

	vRed = vRed.T

	for i in range(numFiles):
		print(filenames[i]),
		for j in range(numFiles):
			print(cosine_similarity(vRed[:,i], vRed[:, j])),
		print("")

	# print(baseArray.shape, 	lowRankArr.shape)

	# for i in range(lowRankArr.shape[1]):
	# 	for j in range(lowRankArr.shape[1]):
