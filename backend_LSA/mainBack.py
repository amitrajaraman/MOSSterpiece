import os
import sys, token, tokenize
import shutil
import re
import numpy as np
import scipy.spatial.distance
from zipfile import ZipFile
import matplotlib
import matplotlib.pyplot as plt
import subprocess

"""
Code for creating heatmap taken from https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html
"""
def heatmap(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

"""
Code for annotating heatmap taken from https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html
"""
def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=["black", "white"], threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

"""
Code for removing comments (from a py file) taken from  https://gist.github.com/BroHui/aca2b8e6e6bdf3cb4af4b246c9837fa3
with minor changes done to bring it into the format we require
"""
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

"""
Code for removing comments (from a CPP file) taken from https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python
Note that we do not necessarily require this due to the code of bashTest.sh, but we keep it in the case that
the code does not compile (so g++ won't work).
Since comments in Java files are similar, we use the same function there as well.
"""
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

"""
This function merely returns the cosine similarity of two vectors (stored as numpy.ndarrays)
We use scipy.spatial distance tosimplify the process
"""
def cosine_similarity(c1, c2):
	if(c1.shape != c2.shape):
		print("ERROR"),
		return ""
	return (1 - scipy.spatial.distance.cosine(c1, c2))

if __name__ == "__main__":

	# Output for the purpose of debugging to ensure that everything works as intended
	print(sys.argv[1])
	print("RUNNING AMIT'S CODE NOW!!!")
	# Location of the (temporary) directory the zip file is unzipped to
	directory = '../backend_LSA/inputDir'
	# Location of the Bash code used for C++ pre-processing
	bashCPP = '../backend_LSA/CPPpreproc.sh'
	bashC = '../backend_LSA/Cpreproc.sh'
	# Location of the output file(s) which store the raw data
	outpFile = '../src/assets/results/outpFile.txt'
	outpCSV = '../src/assets/results/outpFile.csv'
	top = '../src/assets/results/top.txt'
	# Location of the output images
	outpPng = '../src/assets/results/outpImg.png'
	outpHeatmap = '../src/assets/results/outpHeatmap.png'
	# n such that top n results are displayed in the bar graph
	barGraphParam = 10


	# Unzip the argument given to the directory specified by the variable directory (inputDir)
	zipFilePath = ''
	try:
		zipFilePath = sys.argv[1]
		with ZipFile(zipFilePath, 'r') as zipObj:
			zipObj.extractall(directory)
	except:
		print("Usage: mainBack.py relative/path/to/filename.zip")
		print("Quitting")
		quit()

	# Create a list of all the file names as stored in the directory and get the number of files
	filenames = [name for name in os.listdir(directory)]
	numFiles = len(filenames)
	# This variable stores the frequency of each word in each document
	baseDict = {}

	for i in range(numFiles):

		# Create a path to the current file that is being processed
		tempF = os.path.join(directory, filenames[i])
		# Get the extension so we know what pre-processing to apply
		fileExt = (os.path.splitext(tempF))[1]

		### PREPROCESSING

		if(fileExt == '.py'):
			print("Processing "+tempF)
			# Use the function defined above to remove all comments
			comment_remover_py(tempF)
			# Since the output of the function is stored in the file temp, we pipe it back to the normal .py file
			# to make future processing easier and more uniform
			subprocess.call('cat temp > '+tempF, shell=True)
							
		elif(fileExt == '.cpp'):
			print("Processing "+tempF)
			try:
				# Process the CPP file (assuming it compiles) to remove all macros and comments with the output in the file temp
				subprocess.call('bash ' + bashCPP + ' ' + tempF, shell = True)
				# Since the output of the function is stored in the file temp, we pipe it back to the normal .cpp file
				# to make future processing easier and more uniform
				subprocess.call('cat temp > ' + tempF, shell = True)
				# Remove the temporary file (not necessary but we do it anyway)
				subprocess.call('rm temp', shell = True)
			except Exception as e:
				print(e)
				print(tempF + " does not compile.")
			with open(tempF, 'r') as readF:
				f = readF.read()
				# Although unnecessary if it compiles, we remove all comments once again for safety's sake
				f = comment_remover_cpp(f);
				# Write the output back to the cpp file to make future processing more uniform
				with open(tempF, 'w') as writeF:
					writeF.write(f)

		elif(fileExt == '.c'):
			print("Processing "+tempF)
			try:
				# Process the C file (assuming it compiles) to remove all macros and comments with the output in the file temp
				subprocess.call('bash ' + bashC + ' ' + tempF, shell = True)
				# Since the output of the function is stored in the file temp, we pipe it back to the normal .cpp file
				# to make future processing easier and more uniform
				subprocess.call('cat temp > ' + tempF, shell = True)
				# Remove the temporary file (not necessary but we do it anyway)
				subprocess.call('rm temp', shell = True)
			except Exception as e:
				print(e)
				print(tempF + " does not compile.")
			with open(tempF, 'r') as readF:
				f = readF.read()
				# Although unnecessary if it compiles, we remove all comments once again for safety's sake
				f = comment_remover_cpp(f);
				# Write the output back to the c file to make future processing more uniform
				with open(tempF, 'w') as writeF:
					writeF.write(f)


		elif(fileExt == '.java'):
			print("Processing "+tempF)
			with open(tempF, 'r') as readF:
				f = readF.read()
				# Since Java comments are extremely similar to C++ comments, we can use the same function for both
				f = comment_remover_cpp(f);
				# Write the output back to the cpp file to make future processing more uniform
				with open(tempF, 'w') as writeF:
					writeF.write(f)	

		with open(tempF,'r') as readF:
			f = readF.read()
			# Make everything lower case to remove case distinctions
			f = f.lower()
			# Remove all ;s and newlines
			f = f.replace(';', ' ').replace('\n', ' ')
			# Remove all whitespace, returning contiguous blocks with a single space
			f = re.sub(r"\s\s+", ' ', f);
			# f = re.sub('fncall', 'F', f);
			
			# Instantiate the dictionary
			for word in f.split():
				if(word not in baseDict.keys()):
					baseDict[word] = [0] * numFiles
				# Finally, baseDict[word][i] represents the frequency of word in file number i
				baseDict[word][i] += 1

	# Convert it into a numpy array to make future processing simpler
	baseArray = np.array(list(baseDict.values()))
	
	"""
	First, an array is created where the *i,j*th entry represents the occurrence of word *j* in the *i*th document.
	LSA essentially works by detecting the latent similarities between two documents. For example, if the word "dog"
	and "hound" are used similarly in different documents (say we have the sentence "The dog barked at the car" in one
	document and "The hound barked at the car" in another document), then it inherently identifies that the two words
	might mean the same thing. A low-rank approximation of the original array is found by performing Singular Value
	Decomposition and then taking the appropriate rows/columns. When we do this, it clumps together dimensions (which
	are words here) that mean similar things. So if we had the words {(dog),(hound),(bed)} in the original document, a
	low-rank approximation of this could correspond to something like {(1.43*dog + 0.39*hound),(bed)}. That is, when words
	are clumped together, an appropriate weight is given to each word such that it carries latent similarities. After
	these words are grouped together, the cosine similarity between two vectors (in the low-rank approximation) is
	returned as the degree of plagiarism between them.
	"""
	# This particular line performs the SVD part of the algorithm
	u, s, v = np.linalg.svd(baseArray, False)
	# While there is no clear-cut method to pick an optimal rank immediately, we tested quite a bit and this seems to
	# give good results
	lowRank = 1+int((baseArray.shape[0])/5)

	if(lowRank < numFiles):
		lowRank = numFiles+1

	# For extremely large dimension, some research papers seem to suggest that this is a reasonably optimal rank to choose
	# https://www.aclweb.org/anthology/U15-1009.pdf
	if(lowRank > 300):
		lowRank = 300

	# Perform the actual rank-lowering by taking the first lowRank largest singular values
	uRed = u[:lowRank, :]
	sRed = np.diag(s[:lowRank])
	arrRed = np.dot(np.dot(uRed, sRed), v)

	# This array will later store the final degrees of plagiarism
	finalRes = np.zeros((numFiles,numFiles));

	# Not really needed but meh
	arrRed = np.round(arrRed, 7)

	with open(outpFile, 'w') as f:
		for i in range(numFiles):
			# Set diagonal element to 1 since the similarity between two identical files is 1 anyway
			finalRes[i,i] = 1.0
			for j in range(numFiles):
				if(i < j):
					# The degree of plagiarism is just the cosine similarity between the reduced vectors
					finalRes[i,j] = str(cosine_similarity(arrRed[:, i], arrRed[:, j]))	
	"""
	What we noticed is that for CPP or Java files, the general value returned seems to be somewhat high.
	However, there is still a reasonably large divide (~0.1) between actually plagiarised files and files that
	are not plagiarised but return a high value nevertheless.
	This issue is mitigated by raising each element to the 6th power so smaller numbers rapidly dwindle
	whereas the actual plagiarised documents' values remain reasonably high
	"""
	if(fileExt == '.cpp' or fileExt == '.java'):
		finalRes = np.power(finalRes, 6)

	# Write the output into the text file so the website can read it for the live display
	with open(outpFile, 'w') as f:
		for i in range(numFiles):
			f.write(filenames[i]+",")
		f.write("\n")
		for i in range(numFiles):
			finalRes[i,i] = 1.0
			for j in range(numFiles):
				f.write(str(abs(round(finalRes[min(i,j),max(i,j)],3))) + ",")
			f.write("\n")
		
	# Write the output into a CSV in case the user wants to download the results
	with open(outpCSV, 'w') as f:
		for i in range(numFiles):
			f.write(filenames[i]+",")
		f.write("\n")
		for i in range(numFiles):
			finalRes[i,i] = 1.0
			for j in range(numFiles):
				f.write(str(abs(round(finalRes[min(i,j),max(i,j)],3))) + ",")
			f.write("\n")


	# Note that finalRes is an upper triangular matrix.
	# Doing this "mirrors" the array to make it symmetrical throughout
	tempRes = np.array(finalRes, copy=True)
	tempRes = np.maximum(tempRes, tempRes.transpose())
	
	# Set all the diagonal elements to 0 so that they aren't (incorrectly) returned as the pairs
	# that are most similar
	for i in range(numFiles):
		finalRes[i,i] = 0
	

	# Reshape so that we can just use argmax to find the highest similarity
	finalRes = np.reshape(finalRes, (numFiles*numFiles))
	# In case barGraphParam(=10) is more than the number of pairs, then lower it
	numDisp = int(min(barGraphParam, numFiles*(numFiles-1)/2))
	maxInd = [0 for x in range(numDisp)]
	dicTop5 = {}
	for pos in range(numDisp):
		# Find the current highest similarity and immediately set it to 0 so that the same value is not returned again
		# in future iterations
		dicTop5[finalRes[np.argmax(finalRes)]] = str(filenames[np.argmax(finalRes) % numFiles]) + " and " + str(filenames[np.argmax(finalRes) // numFiles])
		finalRes[np.argmax(finalRes)] = 0
	top5Coeffs = [key for key in sorted(dicTop5)]
	top5Names = [dicTop5[key] for key in top5Coeffs]
	
	with open(top, 'w') as f:
		for i in top5Coeffs:
			if(i==top5Coeffs[-1]):
				f.write(str(i))
			else:
				f.write(str(i)+",")
		f.write("\n")
		for i in top5Names:
			if(i==top5Names[-1]):
				f.write(str(i))
			else:
				f.write(str(i)+",")
		f.write("\n")

	# Plot the horizontal bar graph of the top barGraphParam(=10) most similar pairs
	fig, ax = plt.subplots()
	ax.barh(range(len(dicTop5)), top5Coeffs)
	plt.yticks(range(len(dicTop5)), top5Names)


	for index, value in enumerate(top5Coeffs):
		plt.text(value, index, str(round(value,2)))
	# Remove the right margin so that the text does not overflow
	right_side = ax.spines["right"]
	right_side.set_visible(False)

	plt.tight_layout()
	# Print the bar graph image into outpPng
	plt.savefig(outpPng)

	# Create the pretty heatmap
	fig, ax = plt.subplots()
	im, cbar = heatmap(tempRes, filenames, filenames, ax=ax, cmap="BuPu", cbarlabel="Degree of similarity")
	# If there are 15 or more files, then don't annotate the heatmap because that overcrowds the map
	# and makes it look very bad
	if(numFiles < 15):
		texts = annotate_heatmap(im, valfmt="{x:.2f}")

	fig.tight_layout()
	plt.savefig(outpHeatmap)
	
	# Remove all the temporary files created in the process of running the code
	try:
		subprocess.call('rm -r '+directory, shell = True)
		subprocess.call('if [ -f temp ]; then rm temp; fi', shell = True)
	except OSError as error:
		print("Directory does not exist.")