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
# import ast

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


	# subprocess.call('if [ -f '+dest+' ]; then echo '+dest+' found; fi')
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
	print(sys.argv[1])
	print("RUNNING MY CODE NOW!!!")
	# subprocess.call('cd ../backend_LSA')
	# Location of the (temporary) directory the zip file is unzipped to
	directory = '../backend_LSA/inputDir'
	bashLoc = '../backend_LSA/bashTest.sh'
	# subprocess.call('if [[ -d '+directory+' ]]; then rm -r '+directory+'; fi')
	# Location of the output CSV file
	outpFile = '../src/assets/results/outpFile.txt'
	top = '../src/assets/results/top.txt'
	# Location of the output images
	outpPng = '../src/assets/results/outpImg.png'
	outpHeatmap = '../src/assets/results/outpHeatmap.png'
	# n such that top n results are displayed in the bar graph
	barGraphParam = 10


	zipFilePath = ''
	try:
		zipFilePath = sys.argv[1]
		with ZipFile(zipFilePath, 'r') as zipObj:
			zipObj.extractall(directory)
	except:
		print("Usage: mainBack.py relative/path/to/filename.zip")
		print("Quitting")
		quit()
	filenames = [name for name in os.listdir(directory)]
	numFiles = len(filenames)
	baseDict = {}	

	for i in range(numFiles):
		tempF = os.path.join(directory, filenames[i])
		fileExt = (os.path.splitext(tempF))[1]

		### PREPROCESSING
		if(fileExt == '.py'):
			print("Processing "+tempF)
			comment_remover_py(tempF)
			subprocess.call('cat temp > '+tempF, shell=True)
							
		elif(fileExt == '.cpp'):
			print("Processing "+tempF)
			try:
				subprocess.call('bash ' + bashLoc + ' ' + tempF, shell = True)
				subprocess.call('cat temp > ' + tempF, shell = True)
				subprocess.call('rm temp', shell = True)
			except Exception as e:
				print(e)
				print(tempF + " does not compile.")
			with open(tempF, 'r') as readF:
				f = readF.read()
				f = comment_remover_cpp(f);
				with open(tempF, 'w') as writeF:
					writeF.write(f)	
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
			f = re.sub('fncall', 'F', f);
			# print(tempF)
			# print(f)
			for word in f.split():
				if(word not in baseDict.keys()):
					baseDict[word] = [0] * numFiles
				baseDict[word][i] += 1

	baseArray = np.array(list(baseDict.values()))
	
	# print(baseArray.shape)

	u, s, v = np.linalg.svd(baseArray, False)
	lowRank = 1+int((baseArray.shape[0])/5)

	if(lowRank < numFiles):
		lowRank = numFiles+1

	if(lowRank > 300):
		lowRank = 300

	uRed = u[:lowRank, :]
	sRed = np.diag(s[:lowRank])
	arrRed = np.dot(np.dot(uRed, sRed), v)

	finalRes = np.zeros((numFiles,numFiles));

	arrRed = np.round(arrRed, 7)


	with open(outpFile, 'w') as f:
		for i in range(numFiles):
			finalRes[i,i] = 1.0
			for j in range(numFiles):
				if(i < j):
					finalRes[i,j] = str(cosine_similarity(arrRed[:, i], arrRed[:, j]))	
	
	if(fileExt == '.cpp' or fileExt == '.java'):
		finalRes = np.power(finalRes, 6)

	with open(outpFile, 'w') as f:
		for i in range(numFiles):
			f.write(filenames[i]+",")
		f.write("\n")
		for i in range(numFiles):
			finalRes[i,i] = 1.0
			for j in range(numFiles):
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
		dicTop5[finalRes[np.argmax(finalRes)]] = str(filenames[np.argmax(finalRes) % numFiles]) + " and " + str(filenames[np.argmax(finalRes) // numFiles])
		finalRes[np.argmax(finalRes)] = 0
	top5Coeffs = [key for key in sorted(dicTop5)]
	top5Names = [dicTop5[key] for key in top5Coeffs]
	
	fig, ax = plt.subplots()
	ax.barh(range(len(dicTop5)), top5Coeffs)
	plt.yticks(range(len(dicTop5)), top5Names)

	with open(top, 'w') as f:
		for i in top5Coeffs:
			f.write(str(i)+",")
		f.write("\n")
		for i in top5Names:
			f.write(str(i)+",")
		f.write("\n")

	for index, value in enumerate(top5Coeffs):
	    plt.text(value, index, str(round(value,2)))
	right_side = ax.spines["right"]
	right_side.set_visible(False)

	plt.tight_layout()
	plt.savefig(outpPng)

	fig, ax = plt.subplots()
	im, cbar = heatmap(tempRes, filenames, filenames, ax=ax,
                   cmap="BuPu", cbarlabel="Degree of similarity")
	if(numFiles < 15):
		texts = annotate_heatmap(im, valfmt="{x:.2f}")

	fig.tight_layout()
	plt.savefig(outpHeatmap)
	# plt.show()
	# print(top5Coeffs)
	
	try:
		subprocess.call('rm -r '+directory, shell = True)
		subprocess.call('if [ -f temp ]; then rm temp; fi', shell = True)
	except OSError as error:
		print("Directory does not exist.")