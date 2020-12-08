

## Meet the Team

|      Member Name      |                 Contribution to the Project                  |
| :-------------------: | :----------------------------------------------------------: |
|    Amit Rajaraman     | Heavy contribution to the core logic of the project, and the frontend |
| Sudhansh Peddabomma |    Heavy Backend Contribution; login, download and token authentication     |
| Sai Vigna Surapaneni  |  Styling the website, documentation and front end contributions|
|    Akash Cherukuri    | Contributions to frontend, integration of the core logic and the backend|



## Getting Started

This section is dedicated to explain how to run start the website and the backend server. The website uses `Angular10` for the frontend and `Django` for the backend. The website is compatible with all versions of Python from `Python3`.

*Prerequisites:*

- You'll need to install `Angular10`, `npm`, and `NodeJS` for this project to work. The version of `npm` used is `6.14.8`, `Angular` is `10.2.0`, and `NodeJS` is `12.19.0`.
- The versions need not be exactly the same, but if any unintended bugs or the such do pop-up, keep in mind that this might be the reason why.



*Steps to run the code:*

- Clone the repo to your local machine either by doing `git clone <url-of-the-repo>`, or by downloading it directly from github.
- Navigate to the project folder, and open up the terminal (for Ubuntu) or command prompt (for Windows). Create/Activate a virtual environment (optional), and download Django from `requirements.txt` (see the last step).
- Navigate to "DjangoAPI" folder through the virtual-environment-activated-console, and type in the command `python manage.py runserver` to get the Django backend up and running.
- Open another console at the project directory, and type in `npm install all` to make sure that all the required packages are present. Once it is done installing and verifying the packages, do `ng serve --open` to start the frontend. This will start the compilation process of the frontend, and open up the website in your default web browser.
- Install [this](https://chrome.google.com/webstore/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf/related?hl=en) extension for chrome and activate it, to allow CORS requests to be passed.
- Finally, to get the various required Python libraries run ```pip3 install -r requirements.txt``` from your terminal while in the MOSSterpiece directory.

You should be all set up now!

## What has been implemented

- A basic framework for the website has been created.
- Implementation of logging in and registering. Logging in is done using sessions, so that refreshing the page does not log the user out.
- Functionality to changing one's password has been implemented.
- Implemented uploading of files for a user who has logged in. 
- Core logic-wise, the latent semantic analysis strategy has been used. There is also a good amount of pre-processing done if the language of the code is C++, Java, C, or Python.
- The results are displayed after the processing is done, and the overall data is represented using a heatmap and a bargraph. The similarity of any two files can be shown by choosing the appropriate pair using the drop down lists.
- The results (a CSV file with all the similarities, the bar graph, and the heatmap) can be downloaded as a zip file.

## The Theoretical Aspect

The main strategy (among other alternate strategies) we have implemented here is:

- **Latent Semantic Analysis**: This is slightly more polished than the Bag of Words strategy. First, an array is created where the *i,j*th entry represents the occurrence of word *j* in the *i*th document. LSA essentially works by detecting the latent similarities between two documents. For example, if the word "dog" and "hound" are used similarly in different documents (say we have the sentence "The dog barked at the car" in one document and "The hound barked at the car" in another document), then it inherently identifies that the two words might mean the same thing. A low-rank approximation of the original array is found by performing Singular Value Decomposition and then taking the appropriate rows/columns. When we do this, it clumps together dimensions (which are words here) that mean similar things. So if we had the words {(dog),(hound),(bed)} in the original document, a low-rank approximation of this could correspond to something like {(1.43\*dog + 0.39\*hound),(bed)}. That is, when words are clumped together, an appropriate weight is given to each word such that it carries latent similarities. After these words are grouped together, the cosine similarity between two vectors (in the low-rank approximation) is returned as the degree of plagiarism between them.

- While not in use, we have also implemented other strategies, namely
 - **tf-idf**: The _term frequency-inverse document frequency_ algorithm gives a measure of the similarity as follows. If a word occurs multiple times in a single file, then it is probably of relatively higher importance. However, if the word occurs in a large number of documents, then it is probably of less importance (words like ```if``` might occur in high numbers in each individual file, but they also occur in nearly every file and are of less importance). We multiply a measure of these two together to get a reduced vector, using which we take cosine similarities.
 - **Bag-of-words**: This is a very naïve wherein we just get a vector for each file with the word frequencies in decreasing order and take the cosine similarity.

We begin by creating the array used in LSA. In the first case, we just sort each column individually and find cosine similarity. For the second method, we perform the operations described above to get the degree of similarity.

However, before passing the file to the main LSA part of the code, we pre-process the code depending on the language it is in:

* C++: This code compiles the code using ```g++```, but terminates after the pre-processing step. This does two things: remove all macros (such as ```#define``` and ```#include```) and replaces them with the raw code in a file. Sending the output to temp creates a large file with this. Now, we don't want the massive amounts of code which are present because of the replacement of the ```#include``` macros - not replacing them results in a file of over 100000 lines. Going through [the official documentation](https://gcc.gnu.org/onlinedocs/cpp/Preprocessor-Output.html) shows that when we start a section caused by a ```#include```, it should be of the form ```# linenum "library name" 1 3``` and ends with ```# linennum "file name" 2```. Using sed to delete all the intermediate lines, we get what we want. In case the code does not compile, we just use a ```comment_remover_cpp``` function to remove all comments.

* Java: Since the comment format in Java is similar to that of C++, we use the same ```comment_remover_cpp``` function to remove all comments.

* C: We follow the same process as C++ but we use ```gcc``` instead of ```g++```.

* Python: We use a ```comment_remover_py``` function to remove all comments from a Python source file.

* Common pre-processing: We replace contiguous blocks of spaces with a single space and remove all ```;```s.

## Using the Website
 - If you have an account, skip this step. If this is the first time using the website, first register yourself using the `Sign Up` tab, and follow the instructions presented on screen.
 - Login using the `Login` tab, and enter your credentials. If the entered values are correct, you'll be logged in and get redirected to your profile page.
 - On the profile page, you'll be able to:
 	- **Change your Password:** This is to change your password, pretty self-explanatory.
 	- **Process the file :-** Click on this button to be taken to the `Process` tab.
 - Upload a **ZIP File** in which the files to be processed are in the first level. The code will NOT be able to process the zip file if there are folders in it. The code assumes that the zip file is correct, and no sanity check for the zip file has been implemented.
 - Assuming that the format is correct, click on `Process` after the zipfile has been uploaded. This will redirect you to a page where you have to wait until your files have finished processing. **DO NOT REFRESH THE PAGE HERE**
 - After the files have been processed, you will be taken to view the results. Here, there are four sections:
 	- The top ten pairs of files with the highest correlation are displayed (in descending order).
 	- A bargraph and a heatmap of the data is shown for easy visualization of the data (if there are not too many files, then the heatmap is also annotated with the degree of similarity).
 	- Selecting any two files using the dropdown lists and clicking on `Submit` shows the degree of similarity between the files.
 	- The `Download` butto downloads a zip file that containing the graphs and a CSV file (with all the data).
 - After viewing and/or downloading the data, click on the `Process` button on the header if you want to process another zip file.
