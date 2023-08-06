#Import Json elements to encode Python data structures
import json
#Import functions to deal with text
import re, string, unicodedata
#Import nartural language processing functions
import nltk
from nltk import word_tokenize, sent_tokenize
#Import mathematical functions
import numpy as np

# TODO: allow modifications

def getAverageScores(scores):
    avgScores = {"speakers": {}}
    for speaker in scores["speakers"]:
        for entry in scores["speakers"][speaker]:
            if "average" in entry:
                avgScores["speakers"][speaker] = scores["speakers"][speaker][entry]
    return avgScores

# Degree of Participation Measure
#Input: Lists
#output: float
def DPM(speakers, topicControlScores, taskControlScores, disagreementScores, involvementScores):
    DPM = 0
    DPMUsers = {speaker: 0 for speaker in speakers}

    # Update the DPM scores for each user for each function using the calHML function
    # DPM for a speaker is stored as the highest value for the speaker among all of these function calls
    DPMUsers = calHML(topicControlScores, False, DPMUsers)
    DPMUsers = calHML(taskControlScores, False, DPMUsers)
    DPMUsers = calHML(disagreementScores, False, DPMUsers)
    DPMUsers = calHML(involvementScores, True, DPMUsers)
        
    # calculate DPM as an average of the speaker DPMs
    DPM = sum(DPMUsers[speaker] for speaker in DPMUsers)/len(DPMUsers)
    return DPM

# calculate high/med/low for each speakers on LUs
#Input: List, Boolean, Dictionary
#Output: Dictionary
def calHML(scores, isInvolvement, DPMUsers):
    HIGH = 0.8 if isInvolvement else 1
    MED = 0.4 if isInvolvement else 0.5
    LOW = 0

    # get maximum score (first score)
    max_speaker = scores[0][0]
    max_score = scores[0][1]

    # get minimum score (last score)
    min_speaker = scores[-1][0]
    min_score = scores[-1][1]
    
    if (max_score == min_score): # if the scores are the same, then all scores are equal
        if min_score == 0:
            # set DPM of all speakers to LOW   
            DPMUsers = {speaker: max(LOW,DPMUsers[speaker]) for speaker in DPMUsers}
        else:
            # set all to high
            DPMUsers = {speaker: max(HIGH,DPMUsers[speaker]) for speaker in DPMUsers}
    else: # variation exists
        # set DPM of highest speaker to 1 and DPM of lowest speaker to 0
        DPMUsers[max_speaker] = max(1,DPMUsers[max_speaker])
        DPMUsers[min_speaker] = max(0,DPMUsers[min_speaker])
        
        # remove speakers from scores
        scores.pop(0)

        # make sure list isn't empty
        if scores:
            scores.pop()

            if len(scores) > 1: # if more than one speaker left
                first_speaker = scores[0][0]
                first_score = scores[0][1]
                if max_score - first_score < 0.20: # difference of less than 20%, still high
                    DPMUsers[first_speaker] = max(HIGH,DPMUsers[first_speaker])
                else: # otherwise set to medium
                    DPMUsers[first_speaker] = max(MED,DPMUsers[first_speaker])
                scores.pop(0)
            
            # set rest of speakers to medium
            for score in scores:
                DPMUsers[score[0]] = max(MED,DPMUsers[score[0]])
    return DPMUsers

# Persistence of Roles Measure
#Input: speakers List, mesoTopicsSize integer, uttsSize integer, Lists, List weights
#output: float
def PRM(speakers, mesoTopicsSize, uttsSize, topicControlScores, taskControlScores,
    agreementScores, disagreementScores, involvementScores, weights, mesoTopicFloor, dialogueFloor):

    PRM = 0
    PRMUsers = {speaker: 0 for speaker in speakers}

    # if uttsSize OR mesoTopicsSize are within thresholds
    # ! this if statement was switched around in the java code but I think that was a mistake
    if (uttsSize >= dialogueFloor or mesoTopicsSize >= mesoTopicFloor):
        # Update the PRM scores for each user for each function using the calDistance function
        # PRM for a speaker is stored as the highest value for the speaker among all of these function calls
        PRMUsers = calDistance(topicControlScores, weights[0], PRMUsers)
        PRMUsers = calDistance(taskControlScores, weights[1], PRMUsers)
        PRMUsers = calDistance(involvementScores, weights[2], PRMUsers)
        PRMUsers = calDistance(agreementScores, weights[3], PRMUsers)
        PRMUsers = calDistance(disagreementScores, weights[4], PRMUsers)

    # calculate PRM as an average of the speaker PRMs
    PRM = sum(PRMUsers[speaker] for speaker in PRMUsers)/len(PRMUsers)

    return PRM

# takes in input of scores and a weight
#Input: List, Float, Dictionary
#output: Dictionary
def calDistance(scores, weight, PRMUsers):
    # set highest (index 0) to the weight
    last_speaker = scores[0][0]
    last_score = scores[0][1]
    PRMUsers[last_speaker] = max(weight,PRMUsers[last_speaker])

    # if there is more than 1 score
    if len(scores) > 1:
        for i in range(1, len(scores)):
            cur_speaker = scores[i][0]
            cur_score = scores[i][1]

            if last_score - cur_score < 0.20:
                PRMUsers[cur_speaker] = max(weight,PRMUsers[cur_speaker])
            last_score = cur_score

    return PRMUsers

class SocialRoles(object):

    # weights are in order [topicControl, taskControl, involvement, disagreement]
    def Leadership(self,topicControlScores,taskControlScores,involvementScores,disagreementScores,weights=[0.45,0.4,0.05,0.1]):
        result = []
        
        #Get list of speakers
        speakers=list(set([value["speaker"] for value in self.jsonData["turns"]]))

        scores = [
            getAverageScores(topicControlScores), 
            getAverageScores(taskControlScores), 
            getAverageScores(involvementScores), 
            getAverageScores(disagreementScores)]

        # TODO: Investigate why the numbers are ever so slightly off .045->.043 and .24->.239
        for speaker in speakers:
            try:
                result.append((speaker, str(round(np.average([float(score["speakers"][speaker]) for score in scores], weights=weights),3))))
            except ZeroDivisionError:
                result.append((speaker,str(0.0)))

        return result

    # weights are in order [argumentDiversity, networkCentrality, involvement, disagreement]
    def Influencer(self,argumentDiversityScores,networkCentralityScores,topicControlScores,disagreementScores,weights=[0.4,0.5,0.75,0.15]):
        result = []

        #Get list of speakers
        speakers=list(set([value["speaker"] for value in self.jsonData["turns"]]))

        scores = [
            getAverageScores(argumentDiversityScores),
            getAverageScores(networkCentralityScores),
            getAverageScores(topicControlScores),
            getAverageScores(disagreementScores)]

        for speaker in speakers:
            try:
                result.append((speaker, str(round(np.average([float(score["speakers"][speaker]) for score in scores], weights=weights),3))))
            except ZeroDivisionError:
                result.append((speaker,str(0.0)))

        return result

    # weights are in order [topicControl, disagreement, tensionFocus, networkCentrality]
    def PursuitOfPower(self,topicControlScores,disagreementScores,tensionFocusScores,networkCentralityScores,weights=[0.8,0.09,0.02,0.09]):
        result = []

        #Get list of speakers
        speakers=list(set([value["speaker"] for value in self.jsonData["turns"]])) 

        scores = [
            getAverageScores(topicControlScores),
            getAverageScores(disagreementScores),
            getAverageScores(tensionFocusScores),
            getAverageScores(networkCentralityScores)]

        for speaker in speakers:
            try:
                result.append((speaker, str(round(np.average([float(score["speakers"][speaker]) for score in scores], weights=weights),3))))
            except ZeroDivisionError:
                result.append((speaker,str(0.0)))
        return result

    # weights are in order [topicControl, taskControl, involvement, agreement, disagreement]
    def GroupCohesion(self,topicControlScores,taskControlScores,involvementScores,agreementScores,
        disagreementScores,sociabilityScores,taskFocusScores,sociabilityThreshold=0.68,
        taskFocusThreshold=0.32,prmMesoTopicFloor=3,prmDialogueFloor=150,
        prmThreshold=0.75,prmWeights=[1,0.9,0.3,0.7,0.7],dpmThreshold=0.69):

        result = []

        #Get list of speakers
        speakers=list(set([value["speaker"] for value in self.jsonData["turns"]])) 

        scores = [
            getAverageScores(topicControlScores),
            getAverageScores(taskControlScores),
            getAverageScores(involvementScores),
            getAverageScores(agreementScores),
            getAverageScores(disagreementScores),
            getAverageScores(sociabilityScores),
            getAverageScores(taskFocusScores)]

        # Convert dictionaries to lists and sort them from highest to lowest score
        topicControlList = [(speaker, float(scores[0]['speakers'][speaker])) for speaker in scores[0]['speakers']]
        topicControlList.sort(key = lambda x: (-x[1], x[0]))
        taskControlList = [(speaker, float(scores[1]['speakers'][speaker])) for speaker in scores[1]['speakers']]
        taskControlList.sort(key = lambda x: (-x[1], x[0]))
        agreementList = [(speaker, float(scores[2]['speakers'][speaker])) for speaker in scores[2]['speakers']]
        agreementList.sort(key = lambda x: (-x[1], x[0]))
        disagreementList = [(speaker, float(scores[3]['speakers'][speaker])) for speaker in scores[3]['speakers']]
        disagreementList.sort(key = lambda x: (-x[1], x[0]))
        involvementList = [(speaker, float(scores[4]['speakers'][speaker])) for speaker in scores[4]['speakers']]
        involvementList.sort(key = lambda x: (-x[1], x[0]))

        passedThreshold = 0
        total = 4

        # TODO: Add more configurable settings (especially with PRM)
        # get DPM score
        dpmScore = DPM(speakers, topicControlList, taskControlList, disagreementList, involvementList)
        print("done getting DPM:",dpmScore,flush=True)

        # get PRM score
        prmScore = PRM(speakers, len(self.mesoTopicsStanford), len(self.jsonData['turns']),
            topicControlList, taskControlList, agreementList, disagreementList, involvementList, 
            prmWeights,prmMesoTopicFloor,prmDialogueFloor)
        print("done getting PRM:",prmScore,flush=True)

        # compare DPM and PRM
        if dpmScore >= dpmThreshold: passedThreshold += 1
        if prmScore >= prmThreshold: passedThreshold += 1
        
        # compare sociability
        if float(scores[5]["speakers"]["all-users"]) >= sociabilityThreshold: passedThreshold += 1
        # compare task focus
        if float(scores[6]["speakers"]["all-users"]) >= taskFocusThreshold: passedThreshold += 1

        print("GroupCohesion:", passedThreshold/total)
        result.append(('all-users',str(round(passedThreshold/total,3))))

        return result