import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    directory = os.walk(directory)
    mapping = dict()
    for root, _, filenames in directory:
        for filename in filenames:
            mapping[filename] = open(os.path.join(root, filename), 'r').read()
    return mapping
        


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document.lower())
    tokens = [token for token in tokens if (token not in string.punctuation and token not in nltk.corpus.stopwords.words("english"))]
    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    total_docs = len(documents)
    words_set = set(word for sublist in documents.values() for word in sublist)
    for word in words_set:
        documents_containing_word = 0
        for document in documents.values():
            if word in document:
                documents_containing_word += 1
        idfs[word] = math.log(total_docs/documents_containing_word)
    return idfs
            


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    top = dict()
    for file, words in files.items():
        score = 0
        for word in query:
            score += words.count(word) * idfs[word]
        top[file] = score
    return [key for key, value in sorted(top.items(), key=lambda item: item[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    top = list()
    for sentence, words in sentences.items():
        values = [sentence, 0, 0] # sentence, matching word measure, query term density
        for word in query:
            if word in words:
                values[1] += idfs[word]
                values[2] += words.count(word) / len(words)
        top.append(values)
    return [sentence for sentence, mwm, qtd in sorted(top, key=lambda item: (item[1], item[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
