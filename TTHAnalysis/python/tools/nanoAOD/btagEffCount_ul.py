import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from copy import copy, deepcopy
import math
from CMGTools.TTHAnalysis.tools.nanoAOD.constants import _btagWPs

""" These are just some stupid functions to print messages with coloring and all that. Useful for debugging. """
def color_msg(msg, color = "none"):
    """ Prints a message with ANSI coding so it can be printout with colors """
    codes = {
        "none" : "0m",
        "green" : "1;32m",
        "red" : "1;31m",
        "blue" : "1;34m",
        "yellow" : "1;35m"
    }

    print("\033[%s%s \033[0m"%(codes[color], msg))
    return

class bTagEffCount(Module):
    """ Module to compute btagging efficiencies in WZ Run3 """
    def __init__(self, tagger = "DeepFlav", variable = "btagDeepFlavB", year = "2022EE", verbosity = 0): #Default is DeepCSV for 2016
        self.year = year
        self.tagger = tagger
        self.variable = variable
        self.WPs   = ["L", "M", "T"] 
        self.flavors = {
            0 : 'L',
            1 : 'C', 
            2 : 'B'
        }
        self.verbosity = verbosity
        self.listBranches()
        return 
    
    def listBranches(self):
        self.branches = []
        #Now create a passing and failing collection for each wp and flavor
        for wp in self.WPs:
            for fl in self.flavors:
                    self.branches.append(("nJetPassWP%sFL%s"%(wp,self.flavors[fl]),"I"))
                    self.branches.append(("nJetFailWP%sFL%s"%(wp,self.flavors[fl]),"I"))
                    for var in ["pt","eta"]:
                        self.branches.append(("JetFailWP%sFL%s_%s"%(wp,self.flavors[fl], var) ,"F", 20, "nJetFailWP%sFL%s"%(wp,self.flavors[fl])))
                        self.branches.append(("JetPassWP%sFL%s_%s"%(wp,self.flavors[fl], var) ,"F", 20, "nJetPassWP%sFL%s"%(wp,self.flavors[fl])))
        return self.branches
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)
        return
    
    def analyze(self,event):
        ret = self.reset()
        if self.verbosity > 0:
            color_msg("   ---- Analyzing event %d"%(event.event), "green")

        # Clean jets
        cleanjets = [j for j in Collection(event,"JetSel_Recl")]

        for j in cleanjets:
            flav = getattr(j, "hadronFlavour")
            btag = getattr(j, self.variable)
            # Classify jet at gen level
            if flav == 5   : fl = 2
            elif flav == 4 : fl = 1
            else           : fl = 0

            if self.verbosity > 0:
                if fl == 2: origin="B"
                elif fl == 1: origin="C"
                elif fl == 0: origin="Light"
                
                color_msg("    + Classifying a jet of flavor: %d (from %s)"%(fl, origin))
            
            for wp in self.WPs:
                wpname = self.tagger + "_UL%s"%self.year + "_%s"%wp
                passes = "Pass" if btag >= _btagWPs[wpname][1] else "Fail"
                
                if self.verbosity > 0:
                    message="      * Jet %s: %3.2f ---> Passes wp %s (%3.2f)? %s"%(self.tagger, btag, wp, _btagWPs[wpname][1],  "True" if passes == "Pass" else "False")
                    color = "green" if passes == "Pass" else "red"
                        
                    color_msg(message, color)

                ret["nJet%sWP%sFL%s"%(passes, wp, self.flavors[fl])] += 1
                for var in ["pt","eta"]:
                    ret["Jet%sWP%sFL%s_%s"%(passes, wp, self.flavors[fl], var)].append(getattr(j, var))
        writeOutput(self, ret)
        return True 

    def reset(self):
        ret = {}
        for l in self.listBranches():
            if len(l) <= 2: ret[l[0]] = 0
            else: ret[l[0]] = []
        return ret

