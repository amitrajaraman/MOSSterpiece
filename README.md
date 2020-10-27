## The Theoretical Aspect

The two strategies we have attempted to implement here are:

* Naïve Bag of Words strategy: For each document, a sorted vector of the word occurrences in the file are created. The cosine similarity between two vectors is returned as the degree of plagiarism.

* Latent Semantic Analysis: This is slightly more polished than the Bag of Words strategy. First, an array is created where the *i,j*th entry represents the occurrence of the *j*th word in the *i*th document. LSA essentially works by detecting the latent similarities between two documents. For example, if the word "dog" and "hound" are used similarly in different documents (say we have the sentence "The dog barked at the car" in one document and "The hound barked at the car" in another document), then it inherently identifies that the two words might mean the same thing. A low-rank approximation of the original array is found by performing Singular Value Decomposition and then taking the appropriate rows/columns. When we do this, it clumps together dimensions (which are words here) that mean similar things. So if we had the words `{(dog),(hound),(bed)}` in the original document, a low-rank approximation of this could correspond to something like `{(1.43*dog + 0.39*hound),(bed)}`. That is, when words are clumped together, an appropriate weight is given to each word such that it carries latent similarities. After these words are grouped together, the cosine similarity between two vectors (in the low-rank approximation) is returned as the degree of plagiarism between them.

For either method, we begin by creating the array used in LSA. In the first case, we just sort each column individually and find cosine similarity. For the second method, we perform the operations described above to get the degree of similarity.

## Stuff to Implement in the Future

As might be guessed from the name of the project, we plan to implement the algorithm used in the MOSS software (a modified simpler version in case it becomes too challenging to write the actual thing). We have started reading the paper that describes the ideas behind the MOSS algorithm and have also written a brief summary of what is be done as part of the algorithm [here](https://amitrajaraman.github.io/blog/moss)
