import spacy
import ja_ginza

nlp = spacy.load('ja_ginza')
# the root verb of the sentence
root = None
# the root clause of the sentence
rootClause = []
# the sentence being analyzed
doc = None
# the list of all clauses found in the document
clauses = []
# global list of clause heads
clauseHeadList = []

# the main function which will build and return a nested list of clauses within a sentence
def extract_clauses(adoc):
    global root
    global rootClause

    find_root(adoc)

    for child in root.children:
        # if token in child node tagged as a clause head save in separate list to access later
        if child.dep_ in ["advcl", "ccomp"]:
            clauseHeadList.append(child)
        # add the other nodes to the root clause
        else:
            rootClause.extend(traverse_tree(child))
    clauses.append(rootClause)

    # after building root clause iterate through the clause head list to also build those clauses
    for token in clauseHeadList:
        clauses.append(clause_builder(token))

    return clauses


# helper function that traverses tree branches recursively
def traverse_tree(node):
    tokens = [node]
    for child in node.children:
        if child.dep_ in ["advcl", "ccomp"]:
            clauseHeadList.append(child)
        else:
            tokens.extend(traverse_tree(child))
    return tokens


# a helper function that will take in a head node and build a list containing the clause tokens.
def clause_builder(aNode):
    aClause = [aNode]
    for child in aNode.children:
        aClause.extend(traverse_tree(child))
    return aClause


# function to traverse tree and find root
def find_root(aSent):
    global root
    for aToken in aSent:
        if aToken.dep_ == "ROOT":
            root = aToken
            rootClause.append(root)
            break


# function which will return the number of clauses per sentence
def clause_count():
    return len(clauses)


# function which will return the average number of "words" per clause
def wordsp_clause():
    sum = 0
    for clause in clauses:
        sum = sum + len(clause)
    return sum / len(clauses)


# function that returns the list of clauses
def get_clause():
    return clauses


# clear everything for the next sentence to be processed
def clear():
    global root
    global rootClause
    global doc
    global clauses
    global clauseHeadList
    root = None
    # the root clause of the sentence
    rootClause = []
    # the sentence being analyzed
    doc = None
    # the list of all clauses found in the document
    clauses = []
    # global list of clause heads
    clauseHeadList = []
