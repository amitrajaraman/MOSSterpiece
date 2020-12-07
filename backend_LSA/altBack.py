import os
import sys, token, tokenize
import shutil
import re
import numpy as np
import scipy.spatial.distance
from zipfile import ZipFile
import matplotlib.pyplot as plt
# import ast

def comment_remover_py(fname):
	source = open(fname)
	dest = 'temp'
	mod = open(dest, 'w')

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
			mod.write("\n")
		elif toktype == tokenize.COMMENT:
			# Comment
			mod.write("\n")
		else:
			mod.write(ttext)
		prev_toktype = toktype
		last_col = ecol
		last_lineno = elineno


	# os.system('if [ -f '+dest+' ]; then echo '+dest+' found; fi')
	# with open(fname,'wb') as wfd:
	# 	with open('temp','rb') as fd:
	# 		shutil.copyfileobj(fd, wfd)

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
	outpFile = '../src/assets/results/outpFile.csv'
	# Location of the output images
	outpPng = '../src/assets/results/outpImg.png'
	outpHeatmap = '../src/assets/results/outpHeatmap.png'
	# n such that top n results are displayed in the bar graph
	barGraphParam = 10


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

	for i in range(numFiles):
		tempF = os.path.join(directory, filenames[i])
		fileExt = (os.path.splitext(tempF))[1]

		### PREPROCESSING
		if(fileExt == '.py'):
			# try:
			# 	with open(tempF,'r') as f:
			# 		python_code = f.read()
			# 		# root = ast.parse(python_code)
			# 		# names = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
			# 		line = re.sub('\w+(?=\()', 'fnCall', python_code)
			# 	with open(tempF,'w') as f:
			# 		f.write(line)
			# except:
			# 	print(tempF + " does not compile.")
			comment_remover_py(tempF)
			os.system('cat temp > '+tempF)
							
		elif(fileExt == '.cpp'):
			try:
				os.system('bash bashTest.sh ' + tempF)
				os.system('cat temp > ' + tempF)
				os.system('rm temp')
			except Exception as e:
				print(tempF + " does not compile.")
				with open(tempF, 'r') as readF:
					f = readF.read()
					f = comment_remover_cpp(f);
					tempF.write(f)

		elif(fileExt == '.java'):
			print("Processing "+tempF)
			with open(tempF, 'r') as readF:
				f = readF.read()
				f = comment_remover_cpp(f);
				with open(tempF, 'w') as writeF:
					writeF.write(f)	
			
		
		with open(tempF,'r') as readF:

			f = readF.read()
			f = f.lower()
			f = f.replace(';', ' ').replace('\n', ' ')
			f = re.sub(r"\s\s+", ' ', f);
			# f = re.sub('fncall', 'F', f);
			# print(tempF)
			# print(f)
			for word in f.split():
				if(word not in baseDict.keys()):
					baseDict[word] = [0] * numFiles
				baseDict[word][i] += 1

	baseArray = np.array(list(baseDict.values()))
	
	# print(baseArray.shape)

	sumArray = (baseArray > 0)
	sumArray = np.sum(sumArray, axis = 1)
	sumArray = np.log(numFiles / sumArray)
	arrRed = np.log(1+baseArray)
	arrRed = np.multiply(arrRed, arrRed)
	print(arrRed)
	finalRes = np.zeros((numFiles,numFiles));


	arrRed = np.round(arrRed, 7)
	
	with open(outpFile, 'w') as f:
		for i in range(numFiles):
			f.write(filenames[i]+",")
		f.write("\n")
		for i in range(numFiles):
			finalRes[i,i] = 1.0
			for j in range(numFiles):
				if(i < j):
					finalRes[i,j] = str(cosine_similarity(arrRed[:, i], arrRed[:, j]))	
				f.write(str(abs(round(finalRes[min(i,j),max(i,j)],3))) + ",")
			f.write("\n")
	
	
	tempRes = np.array(finalRes, copy=True)
	tempRes = np.maximum(tempRes, tempRes.transpose())
	
	for i in range(numFiles):
		finalRes[i,i] = 0

	
	finalRes = np.reshape(finalRes, (numFiles*numFiles))
	numDisp = int(min(barGraphParam, numFiles*(numFiles-1)/2))
	maxInd = [0 for x in range(numDisp)]
	dicTop5 = {}
	for pos in range(numDisp):
		dicTop5[finalRes[np.argmax(finalRes)]] = str(filenames[np.argmax(finalRes) % numFiles]) + " and\n" + str(filenames[np.argmax(finalRes) // numFiles])
		finalRes[np.argmax(finalRes)] = 0
	top5Coeffs = [key for key in sorted(dicTop5)]
	top5Names = [dicTop5[key] for key in top5Coeffs]
	
	fig, ax = plt.subplots()
	ax.barh(range(len(dicTop5)), top5Coeffs)
	plt.yticks(range(len(dicTop5)), top5Names)

	for index, value in enumerate(top5Coeffs):
	    plt.text(value, index, str(round(value,2)))
	right_side = ax.spines["right"]
	right_side.set_visible(False)

	plt.tight_layout()
	plt.savefig(outpPng)

	fig, ax = plt.subplots()
	# print(finalRes.shape)
	im = ax.imshow(tempRes)

	# We want to show all ticks...
	ax.set_xticks(np.arange(len(filenames)))
	ax.set_yticks(np.arange(len(filenames)))
	# ... and label them with the respective list entries
	ax.set_xticklabels(filenames)
	ax.set_yticklabels(filenames)

	# Rotate the tick labels and set their alignment.
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
	         rotation_mode="anchor")

	# Loop over data dimensions and create text annotations.
	if(numFiles < 15):
		for i in range(numFiles):
		    for j in range(numFiles):
		        text = ax.text(j, i, round(tempRes[i, j],2),
		                       ha="center", va="center", color="w")

	ax.set_title("Heatmap of degree of plagiarism")
	fig.tight_layout()
	# plt.colorbar(plt.pcolor(tempRes))
	plt.savefig(outpHeatmap)
	# print(top5Coeffs)
	
	try:
		os.system('rm -r inputDir')
		os.system('if [ -f temp ]; then rm temp; fi')
	except OSError as error:
		print("Directory does not exist.")