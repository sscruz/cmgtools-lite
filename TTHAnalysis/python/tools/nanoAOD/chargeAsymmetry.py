from math import sqrt, cos
from copy import deepcopy
import struct as st
import warnings as wr
import ROOT as r

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR,deltaPhi
from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from array import array

class chargeAsymmetry(Module):
    def __init__(self):
        self.branches = [ "Top_plus_eta", "Top_plus_y",
                          "Top_minus_eta", "Top_minus_y",
                          "tt_lepton_plus_eta","tt_lepton_plus_y",
                          "tt_lepton_minus_eta","tt_lepton_minus_y",
                      ]

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)

    def isFromTop(self, gen, genparts ):
        while gen.genPartIdxMother >=0:
            if abs(genparts[gen.genPartIdxMother].pdgId) == 6: return 1
            gen = genparts[gen.genPartIdxMother]
        return 0 

    def analyze(self, event):
        results = {}

        # First the parton level stuff
        top_plus = r.TLorentzVector()
        top_minus = r.TLorentzVector()
        if event.Top1_charge > 0:
            top_plus .SetPtEtaPhiM( event.Top1_pt, event.Top1_eta, event.Top1_phi, event.Top1_mass)
            top_minus.SetPtEtaPhiM( event.Top2_pt, event.Top2_eta, event.Top2_phi, event.Top2_mass)
        else:
            top_minus.SetPtEtaPhiM( event.Top1_pt, event.Top1_eta, event.Top1_phi, event.Top1_mass)
            top_plus .SetPtEtaPhiM( event.Top2_pt, event.Top2_eta, event.Top2_phi, event.Top2_mass)

        results["Top_plus_eta"] = top_plus.Eta()
        results["Top_plus_y"] = top_plus.Rapidity()
        results["Top_minus_eta"] = top_minus.Eta()
        results["Top_minus_y"] = top_minus.Rapidity()

        # Now lets deal with the particle level leptons
        all_leps = [l for l in Collection(event,"GenDressedLepton")]
        nLeps = event.nDressSelLep
        iLeps = event.iDressSelLep
        selLeps = [ all_leps[iLeps[i]] for i in xrange(nLeps)]

        all_jets = [l for l in Collection(event,"GenJet")]
        nJets = event.nDressSelJet
        iJets = event.iDressSelJet
        selJets = [all_jets[iJets[i]] for i in xrange(nJets)]

        genparts = [g for g in Collection(event,"GenPart")]
        genleps = [g for g in Collection(event,"GenPart") if abs(g.pdgId) in [11,13]]

        isFiducial=True
        if len(selLeps) < 3: 
            isFiducial=False
        else:
            
            if selLeps[2].pt < 20: # pt of the three greater than 20
                isFiducial=False 
        if len(selJets) < 2: 
            isFiducial=False
        else:
            if selJets[1].pt < 30: 
                isFiducial=False

        
        # if it doesnt pass the fiducial region, we dont care about this (even the reco level)
        if not isFiducial:
            for branch in self.branches:
                results[branch] = -99
        else:
            # lets match dressed leptons with genparts
            fromTop=[]
            for lep in selLeps[:3]:
                matched_particles = []
                for g in genleps:
                    if deltaR(lep,g) < 0.05: # its a match
                        isFromTop = self.isFromTop( g , genparts)
                        if hasattr(lep, 'isFromTop'):
                            if lep.isFromTop !=  isFromTop:
                                print("We are getting a different answer for the two leps")

                        lep.isFromTop =  isFromTop
                if not hasattr(lep, 'isFromTop'):
                    print("Failed to match one lepton")
                    lep.isFromTop = 0

            if sum([lep.isFromTop for lep in selLeps[:3]]) != 2:
                print("We didnt find two tops")
                
            lep_plus = r.TLorentzVector()
            lep_minus = r.TLorentzVector()
            for l in selLeps[:3]:
                if not l.isFromTop: continue
                if l.pdgId < 0 :  # matter has pdgId > 0 but charge < 0 
                    lep_plus.SetPtEtaPhiM( l.pt, l.eta, l.phi, l.mass)
                else:
                    lep_minus.SetPtEtaPhiM( l.pt, l.eta, l.phi, l.mass)

            results["tt_lepton_plus_eta"]  = lep_plus.Eta()
            results["tt_lepton_plus_y"]    = lep_plus.Rapidity()
            results["tt_lepton_minus_eta"] = lep_minus.Eta()
            results["tt_lepton_minus_y"]   = lep_minus.Rapidity()

            


                            
                        


        writeOutput(self, results)

        return True
ChargeAsymmetry = lambda : chargeAsymmetry()
