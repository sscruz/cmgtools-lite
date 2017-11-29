from CMGTools.TTHAnalysis.treeReAnalyzer import *
from PhysicsTools.HeppyCore.utils.deltar import matchObjectCollection3

class FatJets:
    def __init__(self, label="", recllabel='Recl', ptcut = 400, tau32Cut = 0.54, minSDMass=140., maxSDMass=250.):
        self.label     = label
        self.tau32Cut  = tau32Cut 
        self.minSDMass = minSDMass
        self.maxSDMass = maxSDMass
        self.ptcut     = ptcut

    def listBranches(self):
        return [ ("nTaggedJet","I"), ("TaggedJet_iJ","I",10, "nTaggedJet"),
                 ("nFatJet", "I"),
                 ("FatJet_MatchesTop","I",10, "nFatJet"),
                 ("FatJet_MatchesW"  ,"I",10, "nFatJet")]
  
    def __call__(self, event):

        ret = {}
        
        tags = []
        fats = [ fj for fj in Collection(event, "FatJet" , "nFatJet" ) ] 
        tops = [ to for to in Collection(event, "GenTop" , "nGenTop" ) ]
        gens = [ ge for ge in Collection(event, "GenPart", "nGenPart") ]

        topMatch = []; wMatch = []

        for fat in fats:
            # check if theres a top around
            match = False
            for top in tops:
                if deltaR(fat,top) < 0.8: match = True; break 
            topMatch.append( match )

            # check if theres a W around
            match = False
            for w in gens:
                if abs(w.pdgId) != 24: continue
                if deltaR(fat, w) < 0.8: match = True; break
            wMatch.append(match)

            # check if passes top tagging
            if fat.pt < self.ptcut                 : continue
            if fat.tau3 / fat.tau2 < self.tau32Cut : continue
            if fat.softDropMass < self.minSDMass   : continue
            if fat.softDropMass > self.maxSDMass   : continue
        
            tags.append( fats.index(fat) )

        ret['nTaggedJet'       ] = len(tags)
        ret['TaggedJet_iJ'     ] = tags
        ret['nFatJet'          ] = event.nFatJet
        ret['FatJet_MatchesTop'] = topMatch
        ret['FatJet_MatchesW'  ] = wMatch
        
        return ret
