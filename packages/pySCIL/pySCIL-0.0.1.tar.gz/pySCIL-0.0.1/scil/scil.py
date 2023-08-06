# Defines SCIL class
import json

# import from services
from .services import *

# inherit functions from subclasses
class SCIL(_preprocessing.Preprocessing, _topicControl.TopicControl, _taskControl.TaskControl, 
    _agreement.Agreement, _disagreement.Disagreement, _argumentDiversity.ArgumentDiversity, 
    _involvement.Involvement, _networkCentrality.NetworkCentrality, _emotiveLanguageUse.EmotiveLanguageUse, 
    _sociability.Sociability, _tensionFocus.TensionFocus, _taskFocus.TaskFocus, 
    _topicalPositioning.TopicalPositioning, _socialPositioning.SocialPositioning, _socialRoles.SocialRoles):
    
    def __init__(self, jData=None, 
            pTagsStanford=None, aTagsStanford=None, nStanford=None, tStanford=None, mtStanford=None,
            pTagsNLTK=None, aTagsNLTK=None, nNLTK=None, tNLTK=None, mtNLTK=None):

        self.jsonData = jData
        if (jData): 
            self.addJsonData(jData)

        self.posTagsStanford = pTagsStanford
        self.allTagsStanford = aTagsStanford
        self.nounStanford = nStanford
        self.topicsStanford = tStanford
        self.mesoTopicsStanford = mtStanford

        self.posTagsNLTK = pTagsNLTK
        self.allTagsNLTK = aTagsNLTK
        self.nounNLTK = nNLTK
        self.topicsNLTK = tNLTK
        self.mesoTopicsNLTK = mtNLTK

    # perform Stanford preprocessing on json
    def preprocessStanford(self):
        self.stanfordPoSTagger()
        self.NounPosTagsStanford()

    # perform NLTK preprocessing on json
    def preprocessNLTK(self):
        self.NLTKPoSTagger()
        self.NounPosTagsNLTK()

    # need to add data validation but for now just a test
    # takes a json file and attempts to read it as a dictionary, saving to self.jsonData
    def addJsonData(self, data):
        temp = json.load(data)
        if (data != self.jsonData):
            self.posTagsStanford = None
            self.allTagsStanford = None
            self.nounStanford = None
            self.topicsStanford = None
            self.mesoTopicsStanford = None

            self.posTagsNLTK = None
            self.allTagsNLTK = None
            self.nounNLTK = None
            self.topicsNLTK = None
            self.mesoTopicsNLTK = None
        self.jsonData = temp

