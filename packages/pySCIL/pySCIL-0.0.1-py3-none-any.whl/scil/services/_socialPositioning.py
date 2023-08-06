#Import Json elements to encode Python data structures
import json
#Import functions to deal with text
import re, string, unicodedata
#Import nartural language processing functions
import nltk
from nltk import word_tokenize, sent_tokenize
#Import mathematical functions
import numpy as np

# TODO: Re-add comments

class SocialPositioning(object):

    def OfferCommitIndex(self):
        result = []
        offerCommit = []
        offerCommitUsers = {}

        for turn in self.jsonData['turns']:
            if turn["speaker"] not in offerCommitUsers:
                offerCommitUsers[turn["speaker"]] = []
            #MAKE SURE THIS EXISTS
            metaTag, tag = (turn["dialog_act"].lower().split(':') if ":" in turn["dialog_act"] else ("",turn["dialog_act"])) if turn["dialog_act"] != '' else ("","")        
            if tag == "offer-commit":
                offerCommit.append(turn["text"])
                offerCommitUsers[turn["speaker"]].append(turn["text"])

        for user in offerCommitUsers:
            if len(offerCommit) == 0:
                result.append((user,str(0.0)))
            else:
                result.append((user,str(round(len(offerCommitUsers[user])*1.0/len(offerCommit),3))))
        return result

    def ConfirmationRequestIndex(self):
        result = []
        confirmationRequest = []
        confirmationRequestUsers = {}

        for turn in self.jsonData['turns']:
            if turn["speaker"] not in confirmationRequestUsers:
                confirmationRequestUsers[turn["speaker"]] = []

            metaTag, tag = (turn["dialog_act"].lower().split(':') if ":" in turn["dialog_act"] else ("",turn["dialog_act"])) if turn["dialog_act"] != '' else ("","")        
            if tag == "confirmation-request":
                confirmationRequest.append(turn["text"])
                confirmationRequestUsers[turn["speaker"]].append(turn["text"])

        for user in confirmationRequestUsers:
            if len(confirmationRequest) == 0:
                result.append((user,str(0.0)))
            else:
                result.append((user,str(round(len(confirmationRequestUsers[user])*1.0/len(confirmationRequest),3))))
        return result

    def SocialPositioningFunctions(self,weights=[1,1]):
        result={"speakers":{},"error":{"OfferCommitIndex":"",
                                        "ConfirmationRequestIndex":"",
                                        "SocialPositioningFunctions":""}}
        try:
            #Get list of speakers
            speakers=list(set([value["speaker"] for value in self.jsonData["turns"]]))
            #Adequate result structure to the number of speakers
            for speaker in speakers: result["speakers"][speaker]={}

            #Call all the social positioning functions
            try:
                OCI=self.OfferCommitIndex()
            except Exception as e:
                result["error"]["OfferCommitIndex"]=str(e)
                #Default value for Offer Commit Index function
                OCI=[(x,'0.0') for x in  speakers]

            try:
                CRI=self.ConfirmationRequestIndex()
            except Exception as e:
                result["error"]["ConfirmationRequestIndex"]=str(e)
                #Default value for Confirmation Request Index function
                CRI=[(x,'0.0') for x in  speakers]

            
            #Storage the results of the social positioning for each speaker 
            for y,z in zip(OCI,CRI):
                #Storage the functions results
                result["speakers"][y[0]]["OfferCommitIndex"]=y[1]
                result["speakers"][z[0]]["ConfirmationRequestIndex"]=z[1]

            #Calculate the social positioning average for each speaker
            for speaker in result["speakers"]:
                functions=[function for function in result["speakers"][speaker]]
                average = round(np.average([float(result["speakers"][speaker][function]) for function in functions], 
                    weights=weights),3)
                #Storage the average social positioning
                result["speakers"][speaker]["averageSocialPositioning"]=str(average)
            #Return the JSON response              
            return result
        except Exception as e:
            #Handle overall exception
            result["error"]["SocialPositioningFunctions"]=str(e)
            #Return the JSON response
            return result