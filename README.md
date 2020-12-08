

## Meet the Team

|      Member Name      |                 Contribution to the Project                  |
| :-------------------: | :----------------------------------------------------------: |
|    Amit Rajaraman     | Frontend contributions, read-up for core logic implementation |
| Sudhansh Peddabomma |    Heavy Backend Contribution; login, download and merge conflicts     |
| Sai Vigna Surapaneni  |  Front end implementation, Styling the website   |
|    Akash Cherukuri    | Initial Backend and Frontend implementations, Read-up on papers |



## Getting Started

This section is dedicated to explain how to run start the website and the backend server. The website uses `Angular10` for the frontend and `Django` for the backend. The website is compatible with all versions of Python from `Python3`.

*Prerequisites:*

- You'll need to install `Angular10`, `npm`, and `NodeJS` for this project to work. The version of `npm` used is `6.14.8`, `Angular` is `10.2.0`, and `NodeJS` is `12.19.0`.
- The versions need not be exactly the same, but if any unintended bugs or the such do pop-up, keep in mind that this might be the reason why.



*Steps to run the code:*

- Clone the repo to your local machine either by doing `git clone <url-of-the-repo>`, or by downloading it directly from github.
- Navigate to the project folder, and open up the terminal (for Ubuntu) or command prompt (for Windows). Create/Activate a virtual environment (optional), and download Django from `requirements.txt`.
- Navigate to "DjangoAPI" folder through the virtual-environment-activated-console, and type in the command `python manage.py runserver` to get the Django backend up and running.
- Open another console at the project directory, and type in `npm install all` to make sure that all the required packages are present. Once it is done installing and verifying the packages, do `ng serve --open` to start the frontend. This will start the compilation process of the frontend, and open up the website in your default web browser.
- Install [this](https://chrome.google.com/webstore/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf/related?hl=en) extension for chrome and activate it, to allow CORS requests to be passed.




## What has been implemented so far

- A basic framework for the website has been created. 

- Implementation of Logging in and Registering has been done.
- Implemented uploading of files for a user who has logged in.
- Basic implementation for downloading a file has been done. 
- Core logic-wise, a bag-of-words strategy has been used as placeholder logic, which will be replaced later. Rudimentary Latent Semantic Analysis has been implemented as well (debugging is required, some parts don't work as intended).



## The Theoretical Aspect

The main strategy (among other alternate strategies) we have implemented here is:

* **Latent Semantic Analysis**: This is slightly more polished than the Bag of Words strategy. First, an array is created where the *i,j*th entry represents the occurrence of word *j* in the *i*th document. LSA essentially works by detecting the latent similarities between two documents. For example, if the word "dog" and "hound" are used similarly in different documents (say we have the sentence "The dog barked at the car" in one document and "The hound barked at the car" in another document), then it inherently identifies that the two words might mean the same thing. A low-rank approximation of the original array is found by performing Singular Value Decomposition and then taking the appropriate rows/columns. When we do this, it clumps together dimensions (which are words here) that mean similar things. So if we had the words {(dog),(hound),(bed)} in the original document, a low-rank approximation of this could correspond to something like {(1.43\*dog + 0.39\*hound),(bed)}. That is, when words are clumped together, an appropriate weight is given to each word such that it carries latent similarities. After these words are grouped together, the cosine similarity between two vectors (in the low-rank approximation) is returned as the degree of plagiarism between them.

We begin by creating the array used in LSA. In the first case, we just sort each column individually and find cosine similarity. For the second method, we perform the operations described above to get the degree of similarity.

However, before passing the file to the main LSA part of the code, we pre-process the code depending on the language it is in:

* C++: This code compiles the code using ```g++```, but terminates after the pre-processing step. This does two things: remove all macros (such as #define and #include) and replaces them with the raw code in a file. Sending the output to temp creates a large file with this. Now, we don't want the massive amounts of code which are present because of the replacement of the (#include) macros - not replacing them results in a file of over 100000 lines. Going through [the official documentation](https://gcc.gnu.org/onlinedocs/cpp/Preprocessor-Output.html) shows that when we start a section caused by a #include, it should be of the form ```# linenum "library name" 1 3``` and ends with ```# linennum "file name" 2```. Using sed to delete all the intermediate lines, we get what we want. In case the code does not compile, we just use a ```comment_remover_cpp``` function to remove all comments.

* Java: Since the comment format in Java is similar to that of C++, we use the same ```comment_remover_cpp``` function to remove all comments.

* C: We follow the same process as C++ but we use ```gcc``` instead of ```g++```.

* Python: We use a ```comment_remover_py``` function to remove all comments from a Python source file.

* Common pre-processing: We replace contiguous blocks of spaces with a single space and remove all ```;```s.



## Plans on what to implement in the future

- Create file segmentation in the `upload` and the `output` folder, which would let the code pick out the user's particular files.

- Implement sessions for logged in users, a prototype of the same is present as of now.
