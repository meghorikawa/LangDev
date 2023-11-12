import math
import spacy
import clauseExtractor

nlp = spacy.load('ja_ginza')
# global variable to save document text
doctxt = ""
# global variable of list of sentences in document
sentences = []
# global list of coordinating conjunctions list
ccList = []
# global list of subordinating conjunctions
scList = []
# global variable of doc
doc = ""


# function to load the document
def load(aPath):
    file = open(aPath, 'r')
    global doctxt
    global sentences
    global doc
    doctxt = file.read()
    doc = nlp(doctxt)
    sentences = list(doc.sents)

# function to directly load a text (without a file)

def load_text(atext):
    global doctxt
    global doc
    global sentences
    doctxt = atext
    doc = nlp(doctxt)
    sentences = list(doc.sents)

# function to return the average words per sentence in a document
def avgWPS():
    return sum(len(sent) for sent in sentences) / len(sentences)


# function to return the Corrected Type Token Ratio (number of unique words used per text)
# # of tokens over the squ. root of 2* # of words in text.
def cttr():
    # get unique list of words using helper method
    return len(get_uniqueWords()) / (math.sqrt(2 * len(doc)))


# function to return a normalized count per 100 words of subordinating conjunctions
def scFreq():
    scCounter = 0
    wordCount = 0
    for sent in sentences:
        for token in sent:
            if token.pos_ == "SCONJ":
                scCounter += 1
                wordCount += 1
                scList.append(token)
            else:
                wordCount += 1

    return (scCounter / wordCount) * 100


# function to return a normalized count per 100 words of coordinating conjunctions
def ccFreq():
    ccCounter = 0
    wordCount = 0
    for sent in sentences:
        for token in sent:
            if token.pos_ == "CCONJ":
                ccCounter += 1
                wordCount += 1
                ccList.append(token)
            else:
                wordCount += 1

    return (ccCounter / wordCount) * 100


# function to return the list of coordinating conjunctions
def getCCList():
    return ccList


# function to return the list of subordinate clauses
def getSCList():
    return scList


# function to return the average count of words per clause
def words_per_clause():
    # instantiate a list to track each clauses' length
    wpcSum = []

    # first iterate through list of sentences
    for sent in sentences:
        clauseExtractor.extract_clauses(sent)
        # update value of sum
        wpcSum.append(clauseExtractor.wordsp_clause())
        # need to clear after each iteration
        clauseExtractor.clear()
    # return the average of words per clause
    return sum(wpcSum) / len(wpcSum)


# function to return the average count of clauses per sentence
def clauses_per_sentence():
    clauseCountList = []
    for sent in sentences:
        clauseExtractor.extract_clauses(sent)
        clauseCountList.append(clauseExtractor.clause_count())
        # need to clear data after each iteration
        clauseExtractor.clear()
    return sum(clauseCountList) / len(sentences)


def get_sents():
    return len(sentences)


def get_doc_text():
    return doctxt


def get_docLen():
    return len(doc)


def get_sentences():
    return sentences


# helper method to create a list of unique words in the text
def get_uniqueWords():
    seen = set()
    uniqueWord = []
    for token in doc:
        if token.orth not in seen:
            uniqueWord.append(token)
        seen.add(token.orth)
    return uniqueWord


# method to write outputs to SC lists
def write_SClist():
    file = open('/Users/megu/Documents/Tübingen Universität/Language Development/Research Project/SClist.txt', 'a')
    # iterate through the SC list and write to file
    for item in scList:
        file.write(f'{item}\n')
    file.close()
# method to write outputs to CC lists
def write_CClist():
    file = open('/Users/megu/Documents/Tübingen Universität/Language Development/Research Project/CClist.txt', 'a')
    # iterate through the CC list and write to file
    for item in ccList:
        file.write(f'{item}\n')
    file.close()