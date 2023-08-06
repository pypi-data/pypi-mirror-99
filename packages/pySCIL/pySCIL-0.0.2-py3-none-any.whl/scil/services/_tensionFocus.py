#Import Json elements to encode Python data structures
import json
#Import functions to deal with text
import re, string, unicodedata
#Import nartural language processing functions
import nltk
#Import mathematical functions
import numpy as np

# TODO: Re-add comments

class TensionFocus(object):

    def DisagreeRejectTargetIndex(self):
        result=[]

        disagreeTargets = []
        disagreeTargetsUsers = {}

        for turn in self.jsonData['turns']:
            # create entry for each user
            if turn["speaker"] not in disagreeTargetsUsers:
                disagreeTargetsUsers[turn["speaker"]] = []

            # check if tagged as disagree-reject or confirmation-request
            metaTag, tag = (turn["dialog_act"].lower().split(':') if ":" in turn["dialog_act"] else ("",turn["dialog_act"])) if turn["dialog_act"] != '' else ("","")
            linkTo = turn["link_to"].lower()
            if tag == "--disagree-reject" or tag == "confirmation-request":        
                # if citing a specific user (we ignore "all-users" and "")
                if linkTo != "all-users" and linkTo != "":
                    citedUsers = linkTo.split(":")[0] if ":" in linkTo else linkTo
                    citedUsers = citedUsers.split("+") if "+" in citedUsers else [citedUsers]

                    disagreeTargets.append(turn["text"])

                    for citedUser in citedUsers:
                        # ignore self references
                        if citedUser == turn["speaker"]: continue

                        if citedUser not in disagreeTargetsUsers:
                            disagreeTargetsUsers[citedUser] = []
                        disagreeTargetsUsers[citedUser].append(turn["text"])


        # for each user, calculate disagree reject target index
        for user in disagreeTargetsUsers:
            if len(disagreeTargets) == 0:
                result.append((user,str(0.0)))
            else:
                result.append((user,str(round(len(disagreeTargetsUsers[user])*1.0/len(disagreeTargets),3))))
        return result   

    def TopicalDisagreementTargetIndex(self):
        result=[]

        topicalDisagreementTarget = []
        topicalDisagreementTargetUsers = {}
        #0 neutral/unknown, 1 = positive, -1 = negative
        topics = {}
        #6 is link to 7 is polarity 8 is topic

        for turn in self.jsonData['turns']:
            # create entry for each user
            if turn["speaker"] not in topicalDisagreementTargetUsers:
                topicalDisagreementTargetUsers[turn["speaker"]] = []

            citedUsers = []

            # if citing a specific user (we ignore "all-users" and "")
            linkTo = turn["link_to"].lower()
            if linkTo != "all-users" and linkTo != "":
                citedUsers = linkTo.split(":")[0] if ":" in linkTo else linkTo
                citedUsers = citedUsers.split("+") if "+" in citedUsers else [citedUsers]

                for citedUser in citedUsers:
                    # ignore self references
                    if citedUser == turn["speaker"]: continue

                    if citedUser not in topicalDisagreementTargetUsers:
                        topicalDisagreementTargetUsers[citedUser] = []

            topic = turn["topic"].lower()
            if topic not in topics:
                #"" is default person
                topics[topic] = ["", 0]

            changePolar = False
            
            newPolarity = 0

            polarity = turn["polarity"].lower()
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
                topicalDisagreementTarget.append(turn["text"])
                for citedUser in citedUsers:
                    if citedUser == turn["speaker"]: continue

                    topicalDisagreementTargetUsers[citedUser].append(turn["text"])

        # for each user, calculate disagree reject target index
        for user in topicalDisagreementTargetUsers:
            if len(topicalDisagreementTarget) == 0:
                result.append((user,str(0.0)))
            else:
                result.append((user,str(round(len(topicalDisagreementTargetUsers[user])*1.0/len(topicalDisagreementTarget),3))))

        return result  

    def TensionFocusFunctions(self,weights=[1,1]):
        result={"speakers":{},"error":{"DisagreeRejectTargetIndex":"",
                                        "TopicalDisagreementTargetIndex":"",
                                        "TensionFocusFunctions":""}}
        try:
            #Get list of speakers
            speakers=list(set([value["speaker"] for value in self.jsonData["turns"]]))
            #Adequate result structure to the number of speakers
            for speaker in speakers: result["speakers"][speaker]={}

            #Call all the tension focus functions
            try:
                DRT=self.DisagreeRejectTargetIndex()
            except Exception as e:
                result["error"]["DisagreeRejectTargetIndex"]=str(e)
                #Default value for Disagree-Reject Target Index function
                DRT=[(x,'0.0') for x in  speakers]

            try:
                TDT=self.TopicalDisagreementTargetIndex()
            except Exception as e:
                result["error"]["TopicalDisagreementTargetIndex"]=str(e)
                #Default value for Topical Disagreement Target Index function
                TDT=[(x,'0.0') for x in  speakers]

            
            #Storage the results of the tension focus for each speaker 
            for y,z in zip(DRT,TDT):
                #Storage the functions results
                result["speakers"][y[0]]["DisagreeRejectTargetIndex"]=y[1]
                result["speakers"][z[0]]["TopicalDisagreementTargetIndex"]=z[1]

            #Calculate the tension focus average for each speaker
            for speaker in result["speakers"]:
                functions=[function for function in result["speakers"][speaker]]
                average = round(np.average([float(result["speakers"][speaker][function]) for function in functions], 
                    weights=weights),3)
                #Storage the average tension focus
                result["speakers"][speaker]["averageTensionFocus"]=str(average)
            #Return the JSON response              
            return result 
        except Exception as e:
            #Handle overall exception
            result["error"]["TensionFocusFunctions"]=str(e)
            #Return the JSON response
            return result
