from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

from math import sqrt, cos
from copy import copy, deepcopy
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from CMGTools.TTHAnalysis.tools.physicsobjects import _btagWPs
import ROOT as r 
class JetDifferential_vars(Module):
    def __init__(self, label="", recllabel='Recl', doSystJEC=True, variations=[]):
        self.namebranches = [ "mindr_lep1_jet25",
                              "mindr_lep2_jet25",
                              "mindr_lep3_jet25",
                               "dR_lbloose",
                               "dR_lbmedium",
]
     
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.systsJEC = {0:"",\
                         1:"_jesTotalCorrUp"  , -1:"_jesTotalCorrDown",\
                         2:"_jesTotalUnCorrUp", -2: "_jesTotalUnCorrDown",\
                         3:"_jerUp", -3: "_jerDown",\
                     } if doSystJEC else {0:""}
        if len(variations): 
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var
        self.inputlabel = '_'+recllabel
        self.branches = []
        for var in self.systsJEC: self.branches.extend([br+self.label+self.systsJEC[var] for br in self.namebranches])
        if len(self.systsJEC) > 1: 
            self.branches.extend([br+self.label+'_unclustEnUp' for br in self.namebranches if 'met' in br])
            self.branches.extend([br+self.label+'_unclustEnDown' for br in self.namebranches if 'met' in br])


# new interface (nanoAOD-tools)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)
    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection))
        return True


    # logic of the algorithm
    def run(self,event,Collection):
        allret = {}

        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]


        for var in self.systsJEC:
            # prepare output
            ret = dict([(name,0.0) for name in self.namebranches])
            _var = var
            if not hasattr(event,"nJet25"+self.systsJEC[var]+self.inputlabel): 
                _var = 0; 
            jets = [j for j in Collection(event,"JetSel"+self.inputlabel)]
  
            jetptcut =25
            jets = filter(lambda x : getattr(x,'pt%s'%self.systsJEC[_var]) > jetptcut, jets)


            njet = len(jets); nlep = len(leps)
            # fill output
            if njet >= 1:
                ret["mindr_lep1_jet25"] = min([deltaR(j,leps[0]) for j in jets]) if nlep >= 1 else 0;
                ret["mindr_lep2_jet25"] = min([deltaR(j,leps[1]) for j in jets]) if nlep >= 2 else 0;
                ret["mindr_lep3_jet25"] = min([deltaR(j,leps[2]) for j in jets]) if nlep >= 3 else 0;
            else:
                ret['mindr_lep1_jet25'] = -99
                ret['mindr_lep2_jet25'] = -99
                ret['mindr_lep3_jet25'] = -99
            bmedium = filter(lambda x : x.btagDeepFlavB > _btagWPs["DeepFlav_%d_%s"%(event.year,"M")][1], jets)
            bloose  = filter(lambda x : x.btagDeepFlavB > _btagWPs["DeepFlav_%d_%s"%(event.year,"L")][1], jets)
            if len(bmedium) >=1: 
                bmedium.sort(key = lambda x : getattr(x,'pt%s'%self.systsJEC[_var]), reverse = True)
                ret['dR_lbmedium'] = deltaR(bmedium[0],leps[0]) if nlep >= 1 else -99;
            if len(bloose) >=1: 
                bloose.sort(key = lambda x : getattr(x,'pt%s'%self.systsJEC[_var]), reverse = True)
                ret['dR_lbloose'] = deltaR(bloose[0],leps[0]) if nlep >= 1 else -99;
            else:
                ret['dR_lbmedium'] = -99
                ret['dR_lbloose'] = -99
            for br in self.namebranches:
                allret[br+self.label+self.systsJEC[_var]] = ret[br]
	 	
        return allret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2])
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = JetDifferential_vars('','Recl')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
