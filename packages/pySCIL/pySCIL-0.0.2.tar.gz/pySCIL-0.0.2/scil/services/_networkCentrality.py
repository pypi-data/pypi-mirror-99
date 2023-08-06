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

# TODO: Re-add comments

class NetworkCentrality(object):

    def CommunicationLinksMeasure(self):
        result=[]
        communicationLinks = []
        communicationLinksUsers = {}

        for turn in self.jsonData['turns']:
            # create entry for each user
            if turn["speaker"] not in communicationLinksUsers:
                communicationLinksUsers[turn["speaker"]] = []

        
            # if citing a specific user (we ignore "all-users" and "")
            linkTo = turn["link_to"].lower()
            if linkTo != "all-users" and linkTo != "":
                citedUsers = linkTo.split(":")[0] if ":" in linkTo else linkTo
                citedUsers = citedUsers.split("+") if "+" in citedUsers else [citedUsers]

                communicationLinks.append(turn["text"])

                for citedUser in citedUsers:

                    if citedUser not in communicationLinksUsers:
                        communicationLinksUsers[citedUser] = []
                    communicationLinksUsers[citedUser].append(turn["text"])

        # for each user, calculate communication links measure
        for user in communicationLinksUsers:
            if len(communicationLinks) == 0:
                result.append((user,str(0.0)))
            else:
                result.append((user,str(round(len(communicationLinksUsers[user])*1.0/len(communicationLinks),3))))
        return result   

    # TODO RE-ADD CUSTSOMIZABILITY
    def MesoTopicIntroduction(self):
        result=[]

        mesoTopicsUsers = {}
        usedTopics = {}
        # loop through the dialogue
        for turn,topics in zip(self.jsonData['turns'],self.nounStanford):
            # create entry for each user
            if turn["speaker"] not in mesoTopicsUsers:
                mesoTopicsUsers[turn["speaker"]] = []
            for topic in topics:
                # if the user used the mesotopic, add it to their list
                if topic in self.mesoTopicsStanford and topic not in usedTopics:
                    mesoTopicsUsers[turn["speaker"]].append(topic)
                    usedTopics[topic] = 1

        # for each user, calculate the meso topic introduction
        for user in mesoTopicsUsers:
            result.append((user,str(round(len(mesoTopicsUsers[user])*1.0/len(self.mesoTopicsStanford),3))))
        return result    

    def NetworkCentralityFunctions(self,weights=[1,1]):
        result={"speakers":{},"error":{"CommunicationLinksMeasure":"",
                                    "MesoTopicIntroduction":"",
                                    "NetworkCentralityFunctions":""}}
        try:
            #Get list of speakers
            speakers=list(set([value["speaker"] for value in self.jsonData["turns"]]))
            #Adequate result structure to the number of speakers
            for speaker in speakers: result["speakers"][speaker]={}


            #Call all the network centrality functions
            try:
                CLM=self.CommunicationLinksMeasure()
            except Exception as e:
                result["error"]["CommunicationLinksMeasure"]=str(e)
                #Default value for Communication Links Measure function
                CLM=[(x,'0.0') for x in  speakers]
            try:
                MTI=self.MesoTopicIntroduction()
            except Exception as e:
                result["error"]["MesoTopicIntroduction"]=str(e)
                #Default value for Meso Topic Introduction function
                MTI=[(x,'0.0') for x in  speakers]
            
            #Storage the results of the network centrality for each speaker 
            for y,z in zip(CLM,MTI):
                #Storage the functions results
                result["speakers"][y[0]]["CommunicationLinksMeasure"]=y[1]
                result["speakers"][z[0]]["MesoTopicIntroduction"]=z[1]

            #Calculate the network centrality average for each speaker
            for speaker in result["speakers"]:
                functions=[function for function in result["speakers"][speaker]]
                average = round(np.average([float(result["speakers"][speaker][function]) for function in functions], 
                    weights=weights),3)
                #Storage the average network centrality
                result["speakers"][speaker]["averageNetworkCentrality"]=str(average)
            #Return the JSON response              
            return result
        except Exception as e:
            #Handle overall exception
            result["error"]["NetworkCentralityFunctions"]=str(e)
            #Return the JSON response
            return result