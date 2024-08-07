# a class that will calculate the average values of a participant
# will input the directory and then calculate the averages of each doc in the directory....

import WordStats
import os
import statistics
import Participant

# list of the average word count per sentence for each doc
WPS = []
# list of CTTR values
CTTRlist = []
# suboordinating conjunction frequency list
SCfreqlist = []
# coordinating conjunction frequency list
CCfreqlist = []
# words per clause list
WPClist = []
# clauses per sent list
CPSlist = []
# list of CC
CClist = []
# list of SC
SClist = []


# method to calculate the average wps across a participants texts
def calculate(aPath):
    # load text into wordstats
    WordStats.load(aPath)
    # add the words per sent
    WPS.append(WordStats.avgWPS())
    # add the CTTR
    CTTRlist.append(WordStats.cttr())
    # add freq of CC
    CCfreqlist.append(WordStats.ccFreq())
    # add freq of SC
    SCfreqlist.append(WordStats.scFreq())
    # clauses per sent
    CPSlist.append(WordStats.clauses_per_sentence())
    # Clause length (words per clause)
    WPClist.append(WordStats.words_per_clause())
    WordStats.write_SClist()
    WordStats.write_CClist()
    CClist.extend(WordStats.getCCList())
    SClist.extend(WordStats.getSCList())


# return the average WPS
def getWPS():
    return statistics.mean(WPS)

# return average of CC freq
def getCCfreq():
    return statistics.mean(CCfreqlist)

# return average of SC freq
def getSCfreq():
    return statistics.mean(SCfreqlist)

# return average clauses per sent
def getCPS():
    return statistics.mean(CPSlist)

# return average clause length
def getWPC():
    return statistics.mean(WPClist)

# return the average CTTR
def getCTTR():
    return statistics.mean(CTTRlist)

# method to clear lists after each participant
def clear():
    # clear the lists after each participant
    WPS.clear()
    CTTRlist.clear()
    CCfreqlist.clear()
    SCfreqlist.clear()
    CPSlist.clear()
    WPClist.clear()


def getCClist():
    return CClist

def getSClist():
    return SClist


