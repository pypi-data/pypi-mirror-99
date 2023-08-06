#Import Json elements to encode Python data structures
import json
#Import functions to deal with text
import re, string, unicodedata
#Import nartural language processing functions
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
#Import stanford PoS tagger
from nltk.tag import StanfordPOSTagger
#Import mathematical functions
import numpy as np
import copy

# TODO: Re-add comments
# TODO: LET THINGS BE ADJUSTABLE

### GLOBAL VARIABLES
gapSizeCutoff = 10
mesoTopicLengthFloor = 3

def mergeMesoTopics(mesoTopics):
    for mt1 in mesoTopics:
        for mt2 in mesoTopics:
            # skip the same topics
            if mt1 == mt2: continue

            count = 0.0
            for turn in mesoTopics[mt1]:
                if turn in mesoTopics[mt2]:
                    # print("TOPICS",mt1,"and",mt2,"have a shared turn",turn)
                    count += 1

            # if greater than 60% similarity merge topics    
            if (count/len(mesoTopics[mt2])) > 0.3:
                # merge topics
                res = []
                
                i,j = 0,0
                while i < len(mesoTopics[mt1]) and j < len(mesoTopics[mt2]):
                    # ! should we allow duplicate turns, this might make it less likely for topics to be merged
                    # ! should we remove mt2 from the dictionary? the java code doesn't seem to do this
                    if mesoTopics[mt1][i] < mesoTopics[mt2][j]:
                        res.append(mesoTopics[mt1][i])
                        i += 1
                    else:
                        res.append(mesoTopics[mt2][j])
                        j += 1
                res = res + mesoTopics[mt1][i:] + mesoTopics[mt2][j:]

                mesoTopics[mt1] = res
    return mesoTopics

def removeTurnsWithGaps(mesoTopics):
    gsc = gapSizeCutoff #shorten the name
    for topic in mesoTopics:
        i = 0
        while i < len(mesoTopics[topic]):
            if i > 0 and i < len(mesoTopics[topic])-1: # middle elements
                if (mesoTopics[topic][i] - mesoTopics[topic][i-1]) > gsc and \
                    (mesoTopics[topic][i+1] - mesoTopics[topic][i]) > gsc:
                    mesoTopics[topic].pop(i)
                    i -= 1
            elif i == len(mesoTopics[topic])-1 and len(mesoTopics[topic]) > 1: # last element
                if (mesoTopics[topic][i] - mesoTopics[topic][i-1]) > gsc:
                    mesoTopics[topic].pop(i)
            elif i == 0 and len(mesoTopics[topic]) > 1: # first element
                if (mesoTopics[topic][i+1] - mesoTopics[topic][i]) > gsc:
                    mesoTopics[topic].pop(i)
                    i -= 1
            i += 1
    return mesoTopics

def removeShortTopics(mesoTopics):
    return {topic: mesoTopics[topic] for topic in mesoTopics if len(mesoTopics[topic]) >= mesoTopicLengthFloor}

def processMesoTopics(mesoTopicsOld):
    # preprocessing
    mesoTopics = copy.deepcopy(mesoTopicsOld) # deepcopy to not modify the original
    mesoTopics = mergeMesoTopics(mesoTopics)
    mesoTopics = removeTurnsWithGaps(mesoTopics)
    mesoTopics = removeShortTopics(mesoTopics)
    return mesoTopics

class TaskFocus(object):

    def MesotopicStructureMeasure(self):
        result=[]
        mesoTopicsModified = processMesoTopics(self.mesoTopicsStanford)

        # * CALCULATE MSM
        msm = 0
        for topic in mesoTopicsModified:
            start = mesoTopicsModified[topic][0]
            end = mesoTopicsModified[topic][-1]
            mesoLength = end - start

            msm += mesoLength/float(len(self.jsonData['turns']))
        if len(mesoTopicsModified) == 0:
            msm = 0.0
        else:
            msm /= len(mesoTopicsModified)


        # Add msm as a group score
        result.append(('all-users',str(round(msm,3))))
        return result   

    def MesotopicGappingMeasure(self):
        result=[]
        mesoTopicsModified = processMesoTopics(self.mesoTopicsStanford)

        # * CALCULATE MGM
        mgm = 0
        for topic in mesoTopicsModified:
            nonGapLength = len(mesoTopicsModified[topic])
            start = mesoTopicsModified[topic][0]
            end = mesoTopicsModified[topic][-1]
            mesoLength = end-start

            mgm += nonGapLength/float(mesoLength)
        if len(mesoTopicsModified) == 0:
            mgm = 0.0
        else:
            mgm /= len(mesoTopicsModified)


        # Add mgm as a group score
        result.append(('all-users',str(round(mgm,3))))
        return result
            
    def TaskFocusFunctions(self,weights=[1,1]):
        result={"speakers":{},"error":{"MesotopicStructureMeasure":"",
                                        "MesotopicGappingMeasure":"",
                                        "TaskFocusFunctions":""}}
        try:
            result["speakers"]["all-users"]={}

            #Call all the task focus functions
            try:
                MSM=self.MesotopicStructureMeasure()
            except Exception as e:
                result["error"]["MesotopicStructureMeasure"]=str(e)
                #Default value for Meso-topic Structure Measure function
                MSM=[(x,'0.0') for x in speakers]

            try:
                MGM=self.MesotopicGappingMeasure()
            except Exception as e:
                result["error"]["MesotopicGappingMeasure"]=str(e)
                #Default value for Meso-topic Gapping Measure function
                MGM=[(x,'0.0') for x in speakers]

            
            #Storage the results of the task focus for each speaker 
            for y,z in zip(MSM,MGM):
                #Storage the functions results
                result["speakers"][y[0]]["MesotopicStructureMeasure"]=y[1]
                result["speakers"][z[0]]["MesotopicGappingMeasure"]=z[1]

            #Calculate the task focus average for each speaker
            for speaker in result["speakers"]:
                functions=[function for function in result["speakers"][speaker]]
                average = round(np.average([float(result["speakers"][speaker][function]) for function in functions], 
                    weights=weights),3)
                #Storage the average task focus
                result["speakers"][speaker]["averageTaskFocus"]=str(average)
            #Return the JSON response              
            return result
        except Exception as e:
            #Handle overall exception
            result["error"]["TaskFocusFunctions"]=str(e)
            #Return the JSON response
            return result