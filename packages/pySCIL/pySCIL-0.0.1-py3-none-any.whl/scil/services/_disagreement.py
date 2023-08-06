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

class Disagreement(object):

    def DisagreeRejectIndex(self):
        result = []
        disagreeRejects = []
        disagreeRejectsUsers = {}

        for turn in self.jsonData['turns']:
            if turn["speaker"] not in disagreeRejectsUsers:
                disagreeRejectsUsers[turn["speaker"]] = []

            metaTag, tag = (turn["dialog_act"].lower().split(':') if ":" in turn["dialog_act"] else ("",turn["dialog_act"])) if turn["dialog_act"] != '' else ("","")
            if tag == "--disagree-reject":
                disagreeRejects.append(turn["text"])
                disagreeRejectsUsers[turn["speaker"]].append(turn["text"])

        for user in disagreeRejectsUsers:
            if len(disagreeRejects) == 0:
                result.append((user,str(0.0)))
            else:
                result.append((user,str(round(len(disagreeRejectsUsers[user])*1.0/len(disagreeRejects),3))))
        return result

    def TopicalDisagreementIndex(self):
        result=[]

        topicalDisagreement = []
        topicalDisagreementUsers = {}
        #0 neutral/unknown, 1 = positive, -1 = negative
        topics = {}
        #6 is link to 7 is polarity 8 is topic

        for turn in self.jsonData['turns']:
            # create entry for each user
            if turn["speaker"] not in topicalDisagreementUsers:
                topicalDisagreementUsers[turn["speaker"]] = []

            topic, polarity = turn["topic"].lower(), turn["polarity"].lower() 

            if topic not in topics:
                #"" is default person
                topics[topic] = ["", 0]

            changePolar = False
            
            newPolarity = 0

            if polarity == "" or polarity == "neutral":
                newPolarity = 0

            elif polarity == "positive":
                newPolarity = 1

            elif polarity == "negative":
                newPolarity = -1

            if topics[topic][0] != "" and topics[topic][0] != turn["text"] and topics[topic][1] != 0 and topics[topic][1] == -newPolarity:
                changePolar = True

            topics[topic][0] = turn["text"]
            topics[topic][1] = newPolarity

            metaTag, tag = (turn["dialog_act"].lower().split(':') if ":" in turn["dialog_act"] else ("",turn["dialog_act"])) if turn["dialog_act"] != '' else ("","")
            if tag != "--disagree-reject" and changePolar:
                topicalDisagreement.append(turn["text"])

                topicalDisagreementUsers[turn["speaker"]].append(turn["text"])

        # for each user, calculate disagree reject index
        for user in topicalDisagreementUsers:
            if len(topicalDisagreement) == 0:
                result.append((user,str(0.0)))
            else:
                result.append((user,str(round(len(topicalDisagreementUsers[user])*1.0/len(topicalDisagreement),3))))

        return result   

    def DisagreementFunctions(self,weights=[1,1]):
        result={"speakers":{},"error":{"DisagreeRejectIndex":"",
                                    "TopicalDisagreementIndex":"",
                                    "DisagreementFunctions":""}}
        try:
            #Get list of speakers
            speakers=list(set([value["speaker"] for value in self.jsonData["turns"]]))
            #Adequate result structure to the number of speakers
            for speaker in speakers: result["speakers"][speaker]={}

            #Call all the agreement functions
            try:
                DRX = self.DisagreeRejectIndex()
            except Exception as e:
                result["error"]["DisagreeRejectIndex"]=str(e)
                #Default value for Disagree Reject Index function
                DRX=[(x,'0.0') for x in  speakers]

            try:    
                TDX = self.TopicalDisagreementIndex()
            except Exception as e:
                result["error"]["TopicalDisagreementIndex"]=str(e)
                #Default value for Topical Disagreement Index function
                TDX=[(x,'0.0') for x in  speakers]


            #Store the results of the disagreement for each speaker
            for x,z in zip(DRX,TDX):
                #Store the functions results
                result["speakers"][x[0]]["DisagreeRejectIndex"]=x[1]
                result["speakers"][z[0]]["TopicalDisagreementIndex"]=z[1]

            #Calculate the disagreement average for each speaker
            for speaker in result["speakers"]:
                functions = [function for function in result["speakers"][speaker]]
                average = round(np.average([float(result["speakers"][speaker][function]) for function in functions], 
                    weights=weights),3)
                #Store the average disagreement
                result["speakers"][speaker]["averageDisagreement"]=str(average)
            #Return the JSON response
            return result
        except Exception as e:
            #Handle overall exception
            result["error"]["DisagreementFunctions"]=str(e)
            #Return the JSON response
            return result

