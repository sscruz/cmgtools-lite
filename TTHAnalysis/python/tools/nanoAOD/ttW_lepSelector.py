from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

from math import sqrt, cos
from copy import copy, deepcopy
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from CMGTools.TTHAnalysis.tools.physicsobjects import _btagWPs
import ROOT as r 

class ttWLepSelector(Module):
    def __init__(self, recllabel='Recl' ):
        self.inputlabel = '_'+recllabel
        self.branches = [ 
            'lep_pt',
            'lep_eta',
            'lep_phi',
            'm_lb1',
            'm_lb2',
            'dr_lb1',
            'dr_lb2',
            'odd_lep_pt',
            'odd_lep_eta',
            'odd_lep_phi',
            'odd_lep_m_lb1',
            'odd_lep_m_lb2',
            'odd_lep_dr_lb1',
            'odd_lep_dr_lb2',
            'label'
        ] 
        self.label_0 = 0 
        self.label_1 = 0

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)


    def isFromTop(self, l, genparts ):
        gen = genparts[l.genPartIdx]
        while gen.genPartIdxMother >=0:
            if abs(genparts[gen.genPartIdxMother].pdgId) == 6: return 1
            gen = genparts[gen.genPartIdxMother]
        return 0 

    def promptlept(self, l, genparts):
        if (l.genPartFlav not in [1,15]): return False
        if genparts[l.genPartIdx].pdgId*l.pdgId < 0: return False
        return True

    def analyze(self, event):

        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]

        if len(leps) < 3: return False # at least three leptons 
        genparts = [g for g in Collection(event,"GenPart")]


        jets = [j for j in Collection(event,"JetSel"+self.inputlabel)]
        jetptcut = 25
        jets = filter(lambda x : x.pt > jetptcut, jets)
 
        if len(jets) < 2: return False # at least two jets
        bmedium = filter(lambda x : x.btagDeepFlavB > _btagWPs["DeepFlav_%d_%s"%(event.year,"M")][1], jets)
        if len(bmedium) == 0 :  return False # at least one b-jet

        if not all(map( lambda x : self.promptlept(x, genparts), leps[:3])): return False

        all_charge = leps[0].charge + leps[1].charge + leps[2].charge
        if abs(all_charge) != 1: return False

        even_leps = []
        odd_lep=[]
        for il in range(3):
            if leps[il].charge == all_charge: 
                even_leps.append( leps[il] ) 
            else:
                odd_lep.append(leps[il])
        label1 = self.isFromTop( even_leps[0], genparts) 
        label2 = self.isFromTop( even_leps[1], genparts) 

        if label1 + label2 != 1 : 
            return False # this just takes out a few outliers
        
        for lep in even_leps:
            label = self.isFromTop( lep , genparts)
            allret = {}
            allret['lep_pt'] = lep.pt
            allret['lep_phi'] = lep.phi
            allret['lep_eta'] = lep.eta

            allret['odd_lep_pt'] = odd_lep[0].pt
            allret['odd_lep_phi'] = odd_lep[0].phi
            allret['odd_lep_eta'] = odd_lep[0].eta

            if len(bmedium) > 1:
                bjets = bmedium[:2]
            else:
                bjets = [bmedium[0]]
                mindr=99; thejet=None
                for j in jets:
                    if mindr > deltaR(j,lep) and j not in bjets:
                        mindr = deltaR(j,lep)
                        thejet=j
                bjets.append( thejet )
            
                    
            allret['m_lb1'] = (lep.p4()+bjets[0].p4()).M()
            allret['m_lb2'] = (lep.p4()+bjets[1].p4()).M()
            allret['dr_lb1'] = deltaR(lep,bjets[0])
            allret['dr_lb2'] = deltaR(lep,bjets[1])

            allret['odd_lep_m_lb1'] = (odd_lep[0].p4()+bjets[0].p4()).M()
            allret['odd_lep_m_lb2'] = (odd_lep[0].p4()+bjets[1].p4()).M()
            allret['odd_lep_dr_lb1'] = deltaR(odd_lep[0],bjets[0])
            allret['odd_lep_dr_lb2'] = deltaR(odd_lep[0],bjets[1])


            allret['label'] = label
            if label: self.label_1 +=1
            else    : self.label_0 +=1
            writeOutput(self, allret)
            self.wrappedOutputTree.fill()

        return False

ttWlepseletor = lambda : ttWLepSelector()
