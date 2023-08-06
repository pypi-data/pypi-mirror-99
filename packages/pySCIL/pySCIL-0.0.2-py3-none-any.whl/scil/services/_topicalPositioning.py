#Import Json elements to encode Python data structures
import json
#Import functions to deal with text
import re, string, unicodedata
#Import nartural language processing functions
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
#Import mathematical functions
import numpy as np

# TODO: Re-add comments

def getAdjPhrases(pos):
    count = 0
    half_chunk = ""
    # 0 looking for adverb or adjective
    # 1 adverb found looking for adverb or adjective
    # 2 adjective found looking for adjective or noun
    # 3 noun found looking for more
    # if a stage fails, it returns to stage 0
    temp = ""
    stage = 0
    for word, tag in pos:
        failedStage = False
        if (stage == 0):
            if (tag == "RB"):
                stage = 1
                count += 1
            elif (tag == "JJ"):
                stage = 2
                count += 1
            else:
                failedStage = True
        elif (stage == 1):
            if (tag == "RB"):
                count += 1
            elif (tag == "JJ"):
                stage = 2
                count += 1
            else:
                failedStage = True
        elif (stage == 2):
            if (tag == "JJ"):
                count += 1
            elif (re.match(r"NNP?S?", tag)):
                stage = 3
                count += 1
            else:
                failedStage = True
        elif (stage == 3):
            if not (re.match(r"NNP?S?", tag)):
                failedStage = True

        if failedStage:
            if (stage == 3):
                half_chunk += temp + "---"
            else:
                half_chunk += "---"
            count = 0
            stage = 0
            temp = ""
        else:
            temp += word + " "
    half_chunk = re.sub(r"-+","?",half_chunk).split("?")
    half_chunk = [x.strip() for x in half_chunk if x!=""]
    return half_chunk

# TODO: generally improve accuracy 
# TODO?: maybe assume neutral polarities to be positive
# TODO?: maybe keep marked as neutral and assume '' to be positive
# TODO!: include ANEW (or wordnet) topic polarity calculations
# TODO!: make some charts comparing the results of the different options
def getTopicUtterances(jsonData, allTags, mts):
    #turns containing each topic
    topicTurns = {topic: [] for topic in mts}
    infoRequestTurns = {topic: [] for topic in mts}
    responseTurns = []
    agreeTurns = []
    disagreeTurns = []

    topicalPolarityUsers = {}
    
    # pass 1
    # narrow down the search
    for turn, pos in zip(jsonData['turns'],allTags):
        metaTag, tag = (turn["dialog_act"].lower().split(':') if ":" in turn["dialog_act"] else ("",turn["dialog_act"])) if turn["dialog_act"] != '' else ("","")        
        if turn['speaker'] not in topicalPolarityUsers:
            topicalPolarityUsers[turn['speaker']] = {topic: [] for topic in mts}
        
        if tag == "--response-answer":
            responseTurns.append(turn)
        elif tag == "--agree-accept":
            agreeTurns.append(turn)
        elif tag == "--disagree-reject":
            disagreeTurns.append(turn)

        for topic in mts:
            if topic in turn['text']:
                topicTurns[topic].append((turn,pos))
                if tag == "information-request":
                    infoRequestTurns[topic].append(turn["turn_no"])
    
    # pass 2
    for topic in topicTurns:
        for turn, pos in topicTurns[topic]:
            metaTag, tag = (turn["dialog_act"].lower().split(':') if ":" in turn["dialog_act"] else ("",turn["dialog_act"])) if turn["dialog_act"] != '' else ("","")        
            polarity = turn["polarity"].lower() or "neutral"

            # 1st, check if there is response-answer or assertion-opinion
            if (tag == "--response-answer" or tag == "assertion-opinion"):
                topicalPolarityUsers[turn["speaker"]][topic].append((turn["turn_no"],polarity))
                continue
            
            # TODO: improve, check for verb phrases as well
            # 2nd, check if there is adjective/adverb phrase
            phrases = getAdjPhrases(pos)
            if phrases: #if there are adjective/adverb phrases
                topicalPolarityUsers[turn["speaker"]][topic].append((turn["turn_no"],polarity))
                continue

    # pass 3
    # check all response turns, if they respond to an infoRequestTurn, include them
    for turn in responseTurns:            
        linkTo = turn["link_to"].lower()
        if linkTo != "all-users" and linkTo != "":
            citedTurn = linkTo.split(":")[1] if ":" in linkTo else None
            for topic in infoRequestTurns:
                if citedTurn in infoRequestTurns[topic]:
                    polarity = turn["polarity"].lower() or "neutral"
                    topicalPolarityUsers[turn["speaker"]][topic].append((turn["turn_no"],polarity))
                    break

    # pass 4
    # check all agree/disagree responses to the above
    # TODO: Potentially too many utterances happen in these cases? unsure
    for turn in agreeTurns:
        linkTo = turn["link_to"].lower()
        if linkTo != "all-users" and linkTo != "":
            citedUser,citedTurn = linkTo.split(":") if ":" in linkTo else (None,None)
            if citedUser:
                for topic in topicalPolarityUsers[citedUser]:
                    citedPolarity = ''.join([x[1] for x in topicalPolarityUsers[citedUser][topic] if x[0] == citedTurn])
                    topicalPolarityUsers[turn["speaker"]][topic].append((turn["turn_no"],citedPolarity.lower() or "neutral"))
    for turn in disagreeTurns:
        linkTo = turn["link_to"].lower()
        if linkTo != "all-users" and linkTo != "":
            citedUser,citedTurn = linkTo.split(":") if ":" in linkTo else (None,None)
            if citedUser:
                # ? Should we assume neutral to be positive?
                for topic in topicalPolarityUsers[citedUser]:
                    citedPolarity = ''.join([x[1] for x in topicalPolarityUsers[citedUser][topic] if x[0] == citedTurn])
                    if citedPolarity == "neutral":
                        polarity = turn["polarity"].lower() or "neutral"
                    elif citedPolarity == "positive":
                        polarity = "negative"
                    elif citedPolarity == "negative":
                        polarity = "positive"
                    topicalPolarityUsers[turn["speaker"]][topic].append((turn["turn_no"],polarity))                        

    return topicalPolarityUsers

class TopicalPositioning(object):
    topicUtterances = None

    def TopicalPolarityIndex(self):
        # mesoTopics -> self.mesoTopicsStanford

        # detect the following
        # (1) all utterances on T with polarity P applied directly to T using adverb or adjective phrases, or when T is the direct object of a verb
        # (2) all utterances that offer information with polarity P about topic T
        # (3) all responses (agree/disagree acts) to other speakers' statement with polarity P applied to T

        # if 80% or more are positive towards T, TPX = +1
        # if 80% or more are negative towards T, TPX = -1
        # else, TPX = 0

        mts = [topic for topic in self.mesoTopicsStanford]

        result = []

        # call helper function
        if not self.topicUtterances:
            self.topicUtterances = getTopicUtterances(self.jsonData, self.allTagsStanford, mts)

        # calculate TPX
        # TODO: make the threshold customizable
        for user in self.topicUtterances:
            temp = {'topics': {}}
            for topic in self.topicUtterances[user]:
                positive = 0
                negative = 0
                neutral = 0
                for turn in self.topicUtterances[user][topic]:
                    if turn[1] == "positive": 
                        positive += 1
                    elif turn[1] == "negative":
                        negative += 1
                    elif turn[1] == "neutral":
                        neutral += 1
                tot = positive + negative + neutral
                tpx = "0"
                if tot != 0:
                    percentPositive = float(positive) / float(positive + negative + neutral)
                    percentNegative = float(negative) / float(positive + negative + neutral)
                    # print(user,topic,round(percentPositive,3),round(percentNegative,3))
                    if percentPositive >= 0.8:
                        tpx = "1"
                    elif percentNegative >= 0.8:
                        tpx = "-1"
                temp['topics'][topic] = tpx
            result.append((user,temp))

        return result

    def PolarityStrengthIndex(self):
        # calculate the proportion of utterances made on T by this speaker to all
        # utterances made on T. PSX is measured on a 5-point scale corresponding
        # to quintiles in the normal distribution.
        # all utterances (made up of the 3 things we are looking in TPX)
        # > 80% -> 5; > 60% -> 4; > 40% -> 3; > 20% -> 2; >= 0% -> 1

        mts = [topic for topic in self.mesoTopicsStanford]

        result = []

        # call helper function
        if not self.topicUtterances:
            self.topicUtterances = getTopicUtterances(self.jsonData, self.allTagsStanford, mts)

        topicUtterances = {topic: 0 for topic in mts}
        polarityStrengthUsers = {user: {topic: 0 for topic in mts} for user in self.topicUtterances}

        # calculate PSX        
        for topic in mts:
            tot = 0
            for user in self.topicUtterances:
                amt = len(self.topicUtterances[user][topic])
                polarityStrengthUsers[user][topic] = amt
                tot += amt
            topicUtterances[topic] = tot

        for user in polarityStrengthUsers:
            temp = {'topics': {}}
            for topic in polarityStrengthUsers[user]:
                ratio = float(polarityStrengthUsers[user][topic]) / float(topicUtterances[topic])
                percentile = 0
                if ratio <= 0.2:
                    percentile = 1
                elif ratio <= 0.4:
                    percentile = 2
                elif ratio <= 0.6:
                    percentile = 3
                elif ratio <= 0.8:
                    percentile = 4
                else:
                    percentile = 5
                temp['topics'][topic] = str(percentile)
            result.append((user,temp))
        return result

    def TopicalPositioningFunctions(self):
        result={"speakers":{},"error":{"TopicalPolarityIndex":"",
                                        "PolarityStrengthIndex":"",
                                        "TopicalPositioningFunctions":""}}
        try:
            #Get list of speakers
            speakers=list(set([value["speaker"] for value in self.jsonData["turns"]]))
            #Adequate result structure to the number of speakers
            for speaker in speakers: result["speakers"][speaker]={}

            #Call all the tension focus functions
            try:
                TPX=self.TopicalPolarityIndex()
            except Exception as e:
                result["error"]["TopicalPolarityIndex"]=str(e)
                #Default value for Disagree-Reject Target Index function
                TPX=[(x,'0.0') for x in  speakers]
        
            try:
                PSX=self.PolarityStrengthIndex()
            except Exception as e:
                result["error"]["PolarityStrengthIndex"]=str(e)
                #Default value for Topical Disagreement Target Index function
                PSX=[(x,'0.0') for x in  speakers]

            
            #Storage the results of the tension focus for each speaker 
            for y,z in zip(TPX,PSX):
                #Storage the functions results
                result["speakers"][y[0]]["TopicalPolarityIndex"]=y[1]
                result["speakers"][z[0]]["PolarityStrengthIndex"]=z[1]

            #Return the JSON response              
            return result 
        except Exception as e:
            #Handle overall exception
            result["error"]["TopicalPositioningFunctions"]=str(e)
            #Return the JSON response
            return result

