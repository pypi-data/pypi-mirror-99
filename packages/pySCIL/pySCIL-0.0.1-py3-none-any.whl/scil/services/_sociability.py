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

class Sociability(object):

    def ConversationalNormsMeasure(self):
        result=[]

        totalCount = 0
        successCount = 0
        conversationalNorms = {}

        for turn in self.jsonData['turns']:

            metaTag, tag = (turn["dialog_act"].lower().split(':') if ":" in turn["dialog_act"] else ("",turn["dialog_act"])) if turn["dialog_act"] != '' else ("","")
            if tag == "action-directive" or tag == "offer-commit" or tag == "information-request" or tag == "confirmation-request":
                conversationalNorms[turn["turn_no"]] = False
                totalCount += 1

            linkTo = turn["link_to"].lower()
            commActType = turn["comm_act_type"].lower()
            colPosition = linkTo.find(':') 
            if colPosition >= 0 and commActType == 'response-to':

                if linkTo.find('.') >= 0:
                    checkIndex = int(float(linkTo[colPosition + 1:]))
                else:
                    checkIndex = int(linkTo[colPosition + 1:])
                if checkIndex in conversationalNorms and conversationalNorms[checkIndex] == False:
                    conversationalNorms[checkIndex] = True
                    successCount += 1

        if totalCount == 0:
            result.append(('all-users',str(0.0)))
        else:
            result.append(('all-users',str(round(successCount*1.0/totalCount,3))))
        return result   

    def AgreementDisagreementMeasure(self):
        result = []

        #WARNING THIS IS DEPENDENT OF TOPICAL DISAGREEMENT/AGREEMENT
        agreeAmount = 0
        disagreeAmount = 0

        for turn in self.jsonData['turns']:
            metaTag, tag = (turn["dialog_act"].lower().split(':') if ":" in turn["dialog_act"] else ("",turn["dialog_act"])) if turn["dialog_act"] != '' else ("","")    
            #Also need to check amount Topical disagreement
            if tag == "--disagree-reject":
                disagreeAmount += 1

            if tag == "--agree-accept":
                agreeAmount += 1

        result.append(('all-users',str(round((agreeAmount + 1)*1.0/(agreeAmount + disagreeAmount + 1),3))))
        return result

    def NetworkDensityIndex(self):
        networkDensityIndexUsers={}
        localTopicsUsers={}
        users=[]
        result=[]

        for turn,topics in zip(self.jsonData['turns'],self.topicsStanford):
            if turn["text"] == "": continue
            #Save the users on the dialogue
            if turn["speaker"] not in users:
                users.append(turn["speaker"])
            if turn["speaker"] not in networkDensityIndexUsers:
                networkDensityIndexUsers[turn["speaker"]]=0
                
            commActType = turn["comm_act_type"].lower()
            hasBeenAdded = False
            for topic in topics:
                #Save topics related to a speaker mentioned by others
                if topic not in localTopicsUsers:
                    localTopicsUsers[topic]=turn["speaker"]
                    # hasBeenAdded = False
                if turn["speaker"] != localTopicsUsers[topic] and (commActType == "addressed-to" or commActType == "response-to") and not hasBeenAdded:
                    networkDensityIndexUsers[turn["speaker"]] +=1
                    hasBeenAdded = True

        temp = list(networkDensityIndexUsers.values())
        totalMean = np.mean(temp)
        totalSTD = np.std(temp)

        norm = 2*len(self.jsonData['turns'])/(len(users)*(len(users)-1))
        # calculate the Network Density Index
        NDI = (totalMean - totalSTD) / norm

        # result.append(('all-users',(str(round(totalMean,3)), str(round(totalSTD,3)), str(round(norm,3)), str(round(NDI,3)))))
        result.append(('all-users',str(round(NDI,3))))
        return result

    def CiteDisparityIndex(self):
        result=[]

        citationUsers = {} # {user: {cited_by_user: [message]} }

        for turn in self.jsonData['turns']:
            # create dictionary for each user
            if turn["speaker"] not in citationUsers:
                citationUsers[turn["speaker"]] = {}

            # if citing a specific user (we ignore "all-users" and "")
            linkTo = turn["link_to"].lower()
            if linkTo != "all-users" and linkTo != "":
                citedUsers = linkTo.split(":")[0] if ":" in linkTo else linkTo
                citedUsers = citedUsers.split("+") if "+" in citedUsers else [citedUsers]

                # if a message is referring to multiple users
                for citedUser in citedUsers:
                    # in case they site a user who hasn't said anything yet
                    if citedUser not in citationUsers:
                        citationUsers[citedUser] = {}
                    
                    # if citedUser hasn't been cited by current user yet
                    if turn["speaker"] not in citationUsers[citedUser]:
                        citationUsers[citedUser][turn["speaker"]] = []
                    citationUsers[citedUser][turn["speaker"]].append(turn["text"])

        # for each user, calculate cite disparity index
        for userA in citationUsers:
            citeDisparity = {} # {userTo: disparity}
            for userB in citationUsers:
                # skip if users are the same
                if userA == userB: continue

                userA_cites_userB = float(len(citationUsers[userB][userA])) \
                    if userA in citationUsers[userB] else 0.0
                userB_cites_userA = float(len(citationUsers[userA][userB])) \
                    if userB in citationUsers[userA] else 0.0

                # find the citeDisparity between userA and userB 
                # as long as each user cites the other at least once
                if userA_cites_userB*userB_cites_userA != 0:
                    citeDisparity[userB] = userA_cites_userB/userB_cites_userA \
                        if userA_cites_userB >= userB_cites_userA else userB_cites_userA/userA_cites_userB

            # get the average cite disparity between userA and all other users
            if len(citeDisparity) == 0:
                result.append((userA, 0.0))
            else:
                result.append((userA, sum([citeDisparity[user] for user in citeDisparity])/len(citeDisparity)))

        # normalize values based on min and max
        minScore = min(result,key=lambda i:i[1])[1]
        maxScore = max(result,key=lambda i:i[1])[1]

        # calculate CDI as a mean of all user disparities
        CDI = 0
        if (maxScore-minScore) == 0:
            CDI = 1.0
        else:
            CDI = np.mean([(score-minScore)/(maxScore-minScore) for user,score in result])
        result = [('all-users',str(round(CDI,3)))]
        return result

    def SociabilityFunctions(self,weights=[1,1,1,1]):
        result={"speakers":{},"error":{"ConversationalNormsMeasure":"",
                                        "AgreementDisagreementMeasure":"",
                                        "NetworkDensityIndex":"",
                                        "CiteDisparityIndex":"",
                                        "SociabilityFunctions":""}}
        try:
            result["speakers"]["all-users"]={}

            #Call all the sociability functions
            try:
                CNM=self.ConversationalNormsMeasure()
            except Exception as e:
                result["error"]["ConversationalNormsMeasure"]=str(e)
                #Default value for Conversational Norms Measure function
                CNM=[(x,'0.0') for x in  speakers]
            try:
                ADM=self.AgreementDisagreementMeasure()
            except Exception as e:
                result["error"]["AgreementDisagreementMeasure"]=str(e)
                #Default value for Agreement Disagreement Measure function
                ADM=[(x,'0.0') for x in  speakers]
            try:
                NDI=self.NetworkDensityIndex()
            except Exception as e:
                result["error"]["NetworkDensityIndex"]=str(e)
                #Default value for Network Density Index function
                NDI=[(x,'0.0') for x in  speakers]
            try:
                CDI=self.CiteDisparityIndex()
            except Exception as e:
                result["error"]["CiteDisparityIndex"]=str(e)
                #Default value for Cite Disparity Index function
                CDI=[(x,'0.0') for x in  speakers]

            
            #Storage the results of the sociability for each speaker 
            for w,x,y,z in zip(CNM,ADM,NDI,CDI):
                #Storage the functions results
                result["speakers"][w[0]]["ConversationalNormsMeasure"]=w[1]
                result["speakers"][x[0]]["AgreementDisagreementMeasure"]=x[1]
                result["speakers"][y[0]]["NetworkDensityIndex"]=y[1]
                result["speakers"][z[0]]["CiteDisparityIndex"]=str(1-float(z[1])) # for the purpose of calculating average

            #Calculate the sociability average for each speaker
            for speaker in result["speakers"]:
                functions=[function for function in result["speakers"][speaker]]
                average = round(np.average([float(result["speakers"][speaker][function]) for function in functions], 
                    weights=weights),3)
                #Storage the average sociability
                result["speakers"][speaker]["averageSociability"]=str(average)
            #Return the JSON response  

            # change CDI back
            for z in CDI:
                result["speakers"][z[0]]["CiteDisparityIndex"]=z[1]

            return result
        except Exception as e:
            #Handle overall exception
            result["error"]["SociabilityFunctions"]=str(e)
            #Return the JSON response
            return result