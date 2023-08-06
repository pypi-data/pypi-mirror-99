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

class TopicControl(object):

    def LocalTopicIntroduction(self):
        result=[]
        localTopics={}
        localTopicsUsers={}
    
        for turn, topics in zip(self.jsonData['turns'],self.topicsStanford):
            if turn["text"] == "": continue
            #Storage all speakers in the dialogue
            if turn["speaker"] not in localTopicsUsers:
                localTopicsUsers[turn["speaker"]]=[]
            
            for topic in topics:
                #Save the topics associated to each user and all the topics on the dialogue
                if topic not in localTopics:
                    localTopicsUsers[turn["speaker"]].append(topic)
                    localTopics[topic] = 1

        #For each user, calculate the local topic introduction function
        for user in localTopicsUsers:
            result.append((user,str(round(len(localTopicsUsers[user])*1.0/len(localTopics), 3))))
        return result

    def SubsequentMentionsLocalTopics(self):
        localTopicsMentionsUsers={}
        localTopicsMentions={}
        users=[]
        result=[]

        for turn, topics in zip(self.jsonData['turns'],self.topicsStanford):
            if turn["text"] == "": continue
            
            if turn["speaker"] not in users:
                users.append(turn["speaker"])
            if turn["speaker"] not in localTopicsMentionsUsers:
                localTopicsMentionsUsers[turn["speaker"]]={}

            for topic in topics:
                #Save the subsequent mentions of local topics related to a speaker
                if topic in localTopicsMentionsUsers[turn["speaker"]]:
                    localTopicsMentionsUsers[turn["speaker"]][topic]+=1
                else:    
                    localTopicsMentionsUsers[turn["speaker"]][topic]=1
                #Save the all subsequent mentions of local topics   
                if topic in localTopicsMentions:
                    localTopicsMentions[topic]+=1
                else:
                    localTopicsMentions[topic]=1
        
        #Calculate the total number of mentions on the dialogue
        mentions=sum([localTopicsMentions[value] for value in localTopicsMentions.keys()])
        for user in users:
            #For each user calculate his/her total number of mentions
            userMentions=sum([localTopicsMentionsUsers[user][value] for value
                        in localTopicsMentionsUsers[user].keys()])
            result.append((user,str(round(userMentions*1.0/mentions,3))))
        return result   

    def CiteScore(self):
        localTopicsSubsequentMentionsUsers={}
        localTopicsUsers={}
        localTopics={}
        users=[]
        result=[]

        for turn, topics in zip(self.jsonData['turns'],self.topicsStanford):
            if turn["text"] == "": continue
            #Save the users on the dialogue
            if turn["speaker"] not in users:
                users.append(turn["speaker"])
            if turn["speaker"] not in localTopicsSubsequentMentionsUsers:
                localTopicsSubsequentMentionsUsers[turn["speaker"]]={}

            for topic in topics:
                # save topics used in the dialogue
                if topic not in localTopics:
                    localTopics[topic] = 1
                else:
                    localTopics[topic] += 1
                #Save topics related to a speaker mentioned by others
                if topic not in localTopicsUsers:
                    localTopicsUsers[topic]=turn["speaker"]
                    localTopicsSubsequentMentionsUsers[turn["speaker"]][topic]=0
                localTopicUser=localTopicsUsers[topic]
                if turn["speaker"] != localTopicsUsers[topic]:
                    localTopicsSubsequentMentionsUsers[localTopicUser][topic]+=1

        temp=[]
        #Count the number of topic subsequent mentions related to a users
        for user in localTopicsSubsequentMentionsUsers.keys():
            for topic in localTopicsSubsequentMentionsUsers[user].keys():
                temp.append(localTopicsSubsequentMentionsUsers[user][topic])  
        subsequentMentions=sum(temp)
        for user in users:
            #Calculate the all the subsequent mentions on the dialogue
            subsequentUserMentions=sum([localTopicsSubsequentMentionsUsers[user][value]
                                        for value in localTopicsSubsequentMentionsUsers[user].keys()])
            result.append((user,str(round(subsequentUserMentions*1.0/subsequentMentions,3))))
        return result  

    def TurnLength(self):
        usersTurnLength={}
        allTurnLength=0
        result=[]

        for turn in self.jsonData['turns']:
            if turn["text"] == "": continue
            wordsLength=len(turn["text"].split(" "))
            #Save the word length of all dialogue turns
            allTurnLength+=wordsLength
            #Save the word length of all dialogue turns related to a specific user
            if turn["speaker"] not in usersTurnLength:
                usersTurnLength[turn["speaker"]]=wordsLength
            else:    
                usersTurnLength[turn["speaker"]]+=wordsLength
        #For each speaker calculate the turn length        
        for user in usersTurnLength.keys():
            result.append((user,str(round(usersTurnLength[user]*1.0/allTurnLength,3))))
        return result    

    def TopicControlFunctions(self,weights=[1,1,1,1]):
        result={"speakers":{},"error":{"LocalTopicIntroduction":"",
                                    "SubsequentMentionsLocalTopics":"",
                                    "CiteScore":"",
                                    "TurnLength":"",
                                    "TopicControlFunctions":""}}

        try:
            #Get list of speakers
            speakers=list(set([value["speaker"] for value in self.jsonData["turns"]]))
            #Adequate result structure to the number of speakers
            for speaker in speakers: result["speakers"][speaker]={}

            #Call all the topic control functions
            try:
                LTI=self.LocalTopicIntroduction()
            except Exception as e:
                result["error"]["LocalTopicIntroduction"]=str(e)
                #Default value for Local Topic Introduction function
                LTI=[(x,'0.0') for x in  speakers]

            try:    
                SMLT=self.SubsequentMentionsLocalTopics()
            except Exception as e:
                result["error"]["SubsequentMentionsLocalTopics"]=str(e)
                #Default value for Subsequent Mentions Local Topics function
                SMLT=[(x,'0.0') for x in  speakers]
            
            try:
                CS=self.CiteScore()
            except Exception as e:
                result["error"]["CiteScore"]=str(e)
                #Default value for Cite Score function
                CS=[(x,'0.0') for x in  speakers]

            try:
                TL=self.TurnLength()
            except Exception as e:
                result["error"]["TurnLength"]=str(e)
                #Default value for Turn Length function
                TL=[(x,'0.0') for x in  speakers]

            #Storage the results of the topic control for each speaker 
            for w,x,y,z in zip(LTI,SMLT,CS,TL):
                #Storage the functions results
                result["speakers"][w[0]]["LocalTopicIntroduction"]=w[1]
                result["speakers"][x[0]]["SubsequentMentionsLocalTopics"]=x[1]
                result["speakers"][y[0]]["CiteScore"]=y[1]
                result["speakers"][z[0]]["TurnLength"]=z[1]

            #Calculate the topic control average for each speaker
            for speaker in result["speakers"]:
                functions=[function for function in result["speakers"][speaker]]
                average = round(np.average([float(result["speakers"][speaker][function]) for function in functions], 
                    weights=weights),3)
                #Storage the average topic control
                result["speakers"][speaker]["averageTopicControl"]=str(average)
            #Return the JSON response              
            return result
        except Exception as e:
            #Handle overall exception
            result["error"]["TopicControlFunctions"]=str(e)
            #Return the JSON response
            return result
