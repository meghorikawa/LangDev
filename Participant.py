import pandas as pd
import os
import avgCalculator
# create a class to sort the participants by their number and Jcat score with other attributes

# first make list of participants sorted by J-CAT score
participants = []

# list of CC
CClist = []
# list of SC
SClist = []

writinglist = os.listdir('/Users/megu/Documents/Tübingen Universität/Language Development/Research Project/Corpus')

class Participant:

    def __init__(self, name, score):
        self.name = name
        self.score = score
        # average sent length (words per sentence)
        self.WPSavg = 0
        # corrected type token ratio
        self.CTTR = 0
        # frequency of Coordinating Conjunctions per 100 words
        self.CCfreq = 0
        # frequency of subordinating conjunctions per 100 words
        self.SCfreq = 0
        # avg clause length
        self.clauseLen = 0
        # avg clause count per sent
        self.clauseCount = 0

    # the to string method
    def __str__(self):
        return f'Participant: {self.name}  J-Cat Score: {self.score} Words per Sent: {self.WPSavg} CTTR: {self.CTTR}'

def load():
    from pandas import read_excel

    participantListPath = f'/Users/megu/Documents/Tübingen Universität/Language Development/Research Project/ijas_202205_WC.xlsx'

    participantsList = 'ijas_202205_WC.xlsx'
    my_sheet = 'Sheet2'

    # load participant list into pandas
    df = read_excel(participantsList, sheet_name=my_sheet)
    df.dropna(axis=0)
    JCATScore = df[['協力者', 'J-CAT (合計)']]

    for i in JCATScore.index:
        # save data as new Participant
        aParticipantName = JCATScore['協力者'][i]
        if not aParticipantName.__contains__('JJJ') :
            if writinglist.__contains__(aParticipantName):
                aParticipantName = Participant(aParticipantName, JCATScore['J-CAT (合計)'][i])
                # add to participant list
                participants.append(aParticipantName)
        else:
            if writinglist.__contains__(aParticipantName):
                aParticipantName = Participant(aParticipantName, '-')
                participants.append(aParticipantName)


# a method to return a list of participants
def getParticipants():
    return participants

# a method to find a certain participant returns the index that participant is found at in the list
def findParticipant(aName):
    for participant in participants:
        if participant.name == aName:
            return participants.index(participant)
        break

# a method to make the average calculations on the texts in the corpus
def calculateStats():
    for participant in participants:
        update(participant)

# calculate and update the stats for each participant
def update(aParticipant):
    path = f'/Users/megu/Documents/Tübingen Universität/Language Development/Research Project/Corpus/{aParticipant.name}'
    if os.path.isdir(path):
        avgCalculator.calculate(path)
        aParticipant.WPSavg = avgCalculator.getWPS()
        aParticipant.CTTR = avgCalculator.getCTTR()
        aParticipant.CCfreq = avgCalculator.getCCfreq()
        aParticipant.SCfreq = avgCalculator.getSCfreq()
        aParticipant.clauseLen = avgCalculator.getWPC()
        aParticipant.clauseCount = avgCalculator.getCPS()
    else:
        participants.remove(aParticipant)
    avgCalculator.clear()


# return lists of CC and SC used across all texts
def SCCClist():
    CClist = avgCalculator.getCClist()
    SClist = avgCalculator.getSClist()

def saveCClist():
    with open("CClist.txt", "w") as output:
        for item in CClist:
            output.write(str(item) + '\n')

def saveSClist():
    with open("SClist.txt", "w") as output:
        for item in SClist:
            output.write(str(item) + '\n')

def saveList():
    # lists of columns in exported file
    names = [] # participant name
    scores = [] # J-cat Score
    WPSavgs =[] # words per sentence average
    clauseLens = [] # average clause length
    clauseCounts = [] # average clause count
    CCfreqs = [] # freq of Coordinating conjunction per 100 words
    SCfreqs = [] # freq of subordinating conjunction per 100 words
    CTTRs = []   # Correct Type Token Ratio

    for participant in participants:
        names.append(participant.name)
        scores.append(participant.score)
        WPSavgs.append(participant.WPSavg)
        clauseLens.append(participant.clauseLen)
        clauseCounts.append(participant.clauseCount)
        CCfreqs.append(participant.CCfreq)
        SCfreqs.append(participant.SCfreq)
        CTTRs.append(participant.CTTR)

    # convert to pandas df
    dict = {'name': names, 'J-cat Score': scores, 'Sentence Length' : WPSavgs, 'Clause Length': clauseLens, 'Clauses per Sentence': clauseCounts, 'CC Freq':CCfreqs, 'SC Freq': SCfreqs, 'CTTR': CTTRs}
    dfexport = pd.DataFrame(dict)
    dfexport.to_csv('participantData.csv')
    print('data exported')