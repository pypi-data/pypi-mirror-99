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

class Involvement(object):

    def NounPhraseIndex(self):
        result = []

        nounPhrases = []
        nounPhrasesUsers = {}

        for turn,nounTurn in zip(self.jsonData['turns'],self.nounStanford):
            if turn["text"] == "": continue

            # store all speakers in the dialogue
            if turn["speaker"] not in nounPhrasesUsers:
                nounPhrasesUsers[turn["speaker"]] = []
            
            filterWords = {"i", "we", "our", "you", "my", "your", "ourselves",
                "myself", "yourself", "ours", "mine", "yours"}

            # Obtain the noun phrase words for each turn based on PoS tags and filtering out words from above set
            nounPhrasesWords = [noun for noun in nounTurn if noun.lower() not in filterWords]

            for word in nounPhrasesWords:
                # Save the word associated to each user and to all words in discourse
                nounPhrases.append(word)
                nounPhrasesUsers[turn["speaker"]].append(word)

        # For each user, calculate the noun phrase index
        for user in nounPhrasesUsers:
            result.append((user,str(round(len(nounPhrasesUsers[user])*1.0/len(nounPhrases),3))))
        return result

    def TurnIndex(self):
        result = []
        turnIndex = []
        turnIndexUsers = {}

        for turn in self.jsonData['turns']:
            
            turnIndex.append(turn["text"])

            if turn["speaker"] not in turnIndexUsers:
                turnIndexUsers[turn["speaker"]] = []
            turnIndexUsers[turn["speaker"]].append(turn["text"])

        for user in turnIndexUsers:
            result.append((user,str(round(len(turnIndexUsers[user])*1.0/len(turnIndex),3))))
        return result

    def TopicChainIndex(self, gapSizeCutoff=10, mentionPercentageFloor=0.05):
        result = []

        gapSizeCutoff = int(gapSizeCutoff)
        mentionPercentageFloor = float(mentionPercentageFloor)

        #gapSizeCutoff          eg. a new topic will be created if last mention was more than 10 turns ago
        #mentionPercentageFloor eg. only topics with at least 10% of mentions will be included as top topics

        topicChains = {} # dictionary (topic,#chain using this topic): {turn_mentions: []}
        topicChainsUsers = {} # topicChains for each user
        topicMentions = 0 # counts the mentions for topicChains that have at least 2 mentions

        # for each turn in dialogue
        for turn,topics in zip(self.jsonData['turns'],self.topicsStanford):
            # ignore turns with no dialogue
            if turn["text"] == "": continue

            # create a topicChains dictionary for each user
            if turn["speaker"] not in topicChainsUsers:
                topicChainsUsers[turn["speaker"]] = {}

            for topic in topics:
                # if topic is a new topic, create an entry for topicChains and topicChainsUsers
                if (topic,0) not in topicChains:
                    topicChains[(topic,0)] = [float(turn["turn_no"])]
                    topicChainsUsers[turn["speaker"]][(topic,0)] = [float(turn["turn_no"])]
                else:
                    # the bestMatch is the most recent recent chain for the topic
                    bestMatch = (None, -1)
                    i = 0
                    while ((topic, i) in topicChains): 
                        if topicChains[(topic,i)][-1] > bestMatch[1]:
                            bestMatch = (topic,i)
                        i += 1

                    # if turn gap is more than 10, create new topic, else append to bestMatch
                    if ((float(turn["turn_no"]) - topicChains[bestMatch][-1]) > gapSizeCutoff):
                        topicChains[(topic,i)] = [float(turn["turn_no"])]
                        topicChainsUsers[turn["speaker"]][(topic,i)] = [float(turn["turn_no"])]
                    else:
                        topicChains[bestMatch].append(float(turn["turn_no"]))
                        # since we are appending, we need to make sure bestMatch is in topicChainsUsers
                        if bestMatch not in topicChainsUsers:
                            topicChainsUsers[turn["speaker"]][bestMatch] = []
                        topicChainsUsers[turn["speaker"]][bestMatch].append(float(turn["turn_no"]))
                        # count topic mentions (only topic chains >1 can enter above else statement)
                        topicMentions += 2 if len(topicChains[bestMatch]) == 2 else 1

        # CALCULATE THE TOP TOPICS #
        topTopics = [] # stores each occurance of top topics
        topTopicsUsers = {} # stores each occurance of top topic for each user

        for user in topicChainsUsers:
            # create a space in topTopicsUsers for each user
            topTopicsUsers[user] = []
            for topic in topicChains:
                # if the topic forms a chain (more than 1 occurance) and at least 5% of all topic mentions involve this topic
                if len(topicChains[topic]) > 1 and (len(topicChains[topic])*1.0/topicMentions) >= mentionPercentageFloor:
                    # print(topic, topicChains[topic], len(topicChains[topic])*1.0/topicMentions) #prints topics that meet requirements 

                    # add topic to topTopics and topTopicsUsers 
                    topTopics += topicChains[topic]
                    # not every user is guaranteed to have the topic so we need to check to avoid lookup error
                    if topic in topicChainsUsers[user]:
                        topTopicsUsers[user] += topicChainsUsers[user][topic]

        # TODO: Remove test code
        # TEST CODE
        # print(topicMentions)

        # for topic in topicChains:
        #     if topic[0] == "degree":
        #         print(topic, topicChains[topic])


        # for each user, calculate the topic chain index
        for user in topTopicsUsers:
            if len(topTopics) == 0:
                result.append((user,str(0.0)))
            else:
                result.append((user,str(round(len(topTopicsUsers[user])*1.0/len(topTopics),3))))
        return result

    def AllSubsequentMentions(self):
        result = []
        localTopics = set()
        subsequentMentions = []
        subsequentMentionsUsers = {}

        for turn,topics in zip(self.jsonData['turns'],self.topicsStanford):
            # store all speakers in the dialogue
            if turn["speaker"] not in subsequentMentionsUsers:
                subsequentMentionsUsers[turn["speaker"]] = []
            
            if turn["text"] == "": continue
            for topic in topics:
                # if topic has not been mentioned yet, add to set of local topics
                # otherwise add to list of subsequent mentions
                if topic not in localTopics:
                    localTopics.add(topic)
                else:
                    subsequentMentions.append(topic)
                    subsequentMentionsUsers[turn["speaker"]].append(topic)
            
        # For each user, calculate all subsequent mentions measure
        for user in subsequentMentionsUsers:
            result.append((user,str(round(len(subsequentMentionsUsers[user])*1.0/len(subsequentMentions),3))))
        return result

    def AllotopicalityIndex(self):
        result = []
        localTopics = {}
        allotopicalityIndexUsers = {}
        allotopicalityIndexCount = 0
        
        for turn,topicsFound in zip(self.jsonData['turns'],self.topicsStanford):
            if turn["text"] == "": continue

            if turn["speaker"] not in allotopicalityIndexUsers:
                allotopicalityIndexUsers[turn["speaker"]] = 0

            for topic in topicsFound:
                #Save topics related to a speaker mentioned by others
                if topic not in localTopics:
                    localTopics[topic]=turn["speaker"]

                if turn["speaker"] != localTopics[topic]:
                    allotopicalityIndexUsers[turn["speaker"]] += 1
                    allotopicalityIndexCount += 1


        for user in allotopicalityIndexUsers:
            if allotopicalityIndexCount == 0:
                result.append((user, str(round(0 * 1.0/1,3))))
            else:
                result.append((user,str(round(allotopicalityIndexUsers[user]*1.0/allotopicalityIndexCount,3))))
        return result

    def InvolvementFunctions(self,weights=[1,1,1,1,1]):
        result={"speakers":{},"error":{"NounPhraseIndex":"",
                                        "TurnIndex":"",
                                        "TopicChainIndex":"",
                                        "AllSubsequentMentions":"",
                                        "AllotopicalityIndex":"",
                                        "InvolvementFunctions":""}}
        try:
            #Get list of speakers
            speakers=list(set([value["speaker"] for value in self.jsonData["turns"]]))
            #Adequate result structure to the number of speakers
            for speaker in speakers: result["speakers"][speaker]={}

            #Call all the involvement functions
            try:
                NPI=self.NounPhraseIndex()
            except Exception as e:
                result["error"]["NounPhraseIndex"]=str(e)
                #Default value for Noun Phrase Index function
                NPI=[(x,'0.0') for x in speakers]

            try:
                TI=self.TurnIndex()
            except Exception as e:
                result["error"]["TurnIndex"]=str(e)
                #Default value for Turn Index function
                TI=[(x,'0.0') for x in speakers]

            try:
                #TODO: RE-ADD CUSTOMIZATION
                TCI=self.TopicChainIndex()
            except Exception as e:
                result["error"]["TopicChainIndex"]=str(e)
                #Default value for Topic Chain Index function
                TCI=[(x,'0.0') for x in speakers]

            try:
                ASM=self.AllSubsequentMentions()
            except Exception as e:
                result["error"]["AllSubsequentMentions"]=str(e)
                #Default value for All Subsequent Mentions function
                ASM=[(x,'0.0') for x in speakers]

            try:
                ATP=self.AllotopicalityIndex()
            except Exception as e:
                result["error"]["AllotopicalityIndex"]=str(e)
                #Default value for Allotopicality Index function
                ATP=[(x,'0.0') for x in speakers]

            #Store the results of the agreement for each speaker
            for v,w,x,y,z in zip(NPI,TI,TCI,ASM,ATP):
                #Store the functions results
                result["speakers"][v[0]]["NounPhraseIndex"]=v[1]
                result["speakers"][w[0]]["TurnIndex"]=w[1]
                result["speakers"][x[0]]["TopicChainIndex"]=x[1]
                result["speakers"][y[0]]["AllSubsequentMentions"]=y[1]
                result["speakers"][z[0]]["AllotopicalityIndex"]=z[1]

            #Calculate the involvement average for each speaker
            # print(settings)
            for speaker in result["speakers"]:
                functions = [function for function in result["speakers"][speaker]]
                average = round(np.average([float(result["speakers"][speaker][function]) for function in functions], 
                    weights=weights),3)
                #Store the average involvement
                result["speakers"][speaker]["averageInvolvement"]=str(average)
            #Return the JSON response
            return result
        except Exception as e:
            #Handle overall exception
            result["error"]["InvolvementFunctions"]=str(e)
            #Return the JSON response
            return result