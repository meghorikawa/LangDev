import pandas as pd
import os
import avgCalculator
import re

# Create a class to sort the participants by their number and JCAT score with other attributes

# First make list of participants sorted by J-CAT score
participants = []

# List of CC
CClist = []
# List of SC
SClist = []

writinglist = os.listdir('/Users/megu/Documents/Tübingen Universität/Language Development/Research Project/Corpus')

class Participant:

    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.tasks = []
        # Average sent length (words per sentence)
        self.WPSavg = 0
        # Corrected type token ratio
        self.CTTR = 0
        # Frequency of Coordinating Conjunctions per 100 words
        self.CCfreq = 0
        # Frequency of subordinating conjunctions per 100 words
        self.SCfreq = 0
        # Avg clause length
        self.clauseLen = 0
        # Avg clause count per sent
        self.clauseCount = 0

    # The to string method
    def __str__(self):
        return f'Participant: {self.name} J-Cat Score: {self.score} Words per Sent: {self.WPSavg} CTTR: {self.CTTR}'

def load():
    from pandas import read_excel

    participantListPath = f'/Users/megu/Documents/Tübingen Universität/Language Development/Research Project/ijas_202205_WC.xlsx'

    participantsList = 'ijas_202205_WC.xlsx'
    my_sheet = 'Sheet2'

    # Load participant list into pandas
    df = read_excel(participantsList, sheet_name=my_sheet)
    df.dropna(axis=0)
    JCATScore = df[['協力者', 'J-CAT (合計)']]

    for i in JCATScore.index:
        # Save data as new Participant
        aParticipantName = JCATScore['協力者'][i]
        if not aParticipantName.__contains__('JJJ'):
            if writinglist.__contains__(aParticipantName):
                aParticipant = Participant(aParticipantName, JCATScore['J-CAT (合計)'][i])
                # Add to participant list
                participants.append(aParticipant)
        else:
            if writinglist.__contains__(aParticipantName):
                aParticipant = Participant(aParticipantName, '999')
                participants.append(aParticipant)

# A method to return a list of participants
def getParticipants():
    return participants

# A method to find a certain participant returns the index that participant is found at in the list
def findParticipant(aName):
    for participant in participants:
        if participant.name == aName:
            return participants.index(participant)
    return -1

# A method to make the average calculations on the texts in the corpus
def calculateStats():
    for participant in participants:
        update(participant)

# Calculate and update the stats for each participant
def update(aParticipant):
    path = f'/Users/megu/Documents/Tübingen Universität/Language Development/Research Project/Corpus/{aParticipant.name}'
    if os.path.isdir(path):
        # Return list of files in directory
        files_list = os.listdir(path)
        for file in files_list:
            new_path = f'{path}/{file}'
            avgCalculator.calculate(new_path)
            task = get_task(file)
            aParticipant.tasks.append({
                'task': task,
                'WPSavg': avgCalculator.getWPS(),
                'CTTR': avgCalculator.getCTTR(),
                'CCfreq': avgCalculator.getCCfreq(),
                'SCfreq': avgCalculator.getSCfreq(),
                'clauseLen': avgCalculator.getWPC(),
                'clauseCount': avgCalculator.getCPS()
            })
    else:
        participants.remove(aParticipant)
    avgCalculator.clear()

def get_task(file_name):
    pattern = r'_(\w{1,2})\.txt$'
    match = re.search(pattern, file_name)
    if match is not None:
        return match.group(1)
    else:
        return None

# Return lists of CC and SC used across all texts
def SCCClist():
    global CClist, SClist
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
    # Lists of columns in exported file
    participant_data = []

    for participant in participants:
        for task in participant.tasks:
            participant_data.append({
                'name': participant.name,
                'J-cat Score': participant.score,
                'task': task['task'],
                'Sentence Length': task['WPSavg'],
                'Clause Length': task['clauseLen'],
                'Clauses per Sentence': task['clauseCount'],
                'CC Freq': task['CCfreq'],
                'SC Freq': task['SCfreq'],
                'CTTR': task['CTTR']
            })

    # Convert to pandas df
    dfexport = pd.DataFrame(participant_data)
    dfexport.to_csv('participantData.csv', index=False)
    print('data exported')

# Ensure to call the appropriate functions in your workflow
load()
calculateStats()
saveList()
