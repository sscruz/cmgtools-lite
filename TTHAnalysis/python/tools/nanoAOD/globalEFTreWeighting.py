from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
import os, sys
import math
import numpy as np 
import imp
import tempfile, shutil
import numpy
import json 

def invert_momenta(p):
    #fortran/C-python do not order table in the same order
    new_p = []
    for i in range(len(p[0])):  
        new_p.append([0]*len(p))
    for i, onep in enumerate(p):
        for j, x in enumerate(onep):
            new_p[j][i] = x
    return new_p

def SortPDGs(pdgs):
    return sorted(pdgs[:2]) + sorted(pdgs[2:])


def zboost(part, pboost=[]):
    """Both momenta should be in the same frame.
The boost perform correspond to the boost required to set pboost at
    rest (only z boost applied).
    """
    E = pboost[0]
    pz = pboost[3]
    #beta = pz/E
    gamma = E / math.sqrt(E**2-pz**2)
    gammabeta = pz  / math.sqrt(E**2-pz**2)
        
    out =  [gamma * part[0] - gammabeta * part[3],
            part[1],
            part[2],
            gamma * part[3] - gammabeta * part[0]]
    
    if abs(out[3]) < 1e-6 * out[0]:
        out[3] = 0
    return out


def numToString(num):
    return ("%4.2f"%num).replace('.','p').replace('-','m')
        
class globalEFTreWeighting( Module ):
    def __init__(self, process):

        self.process_dict = { 
            'tHq' : "tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
            'tllq' : "tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
            'ttH' : "ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
            'ttll' : "ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
            'ttln' : "ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
            'tttt' : "tttt_FourtopsMay3v1_run0",
        }
        self.WCs_per_process = eval( open(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/global_eft/selectedWCs.txt').read())
        self.mods=[]
        self.tmpdirs=[]
        self.tmpdir='/scratch/'
        
        path=os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/global_eft/%s/SubProcesses'%self.process_dict[process]
        

        # reweighting points (first should be reference) 
        self.param_cards=[os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/global_eft/param_card_%s.dat'%process]
        self.all_WCs=['cQlMi', 'ctq8', 'ctli', 'cpQM', 'cQq81', 'cQl3i', 'ctlTi', 'cQei', 'ctG', 'ctp', 'cptb', 'cQq13', 'ctZ', 'ctW', 'ctei', 'cpQ3', 'cbW', 'ctt1', 'cQq83', 'cQq11', 'cQQ1', 'cpt', 'ctlSi', 'cQt1', 'cQt8', 'ctq1']

        # generate scan
        param_card_template = open(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/global_eft/param_card_template_%s.dat'%process).read()
        wc_dict = dict( [(wc, '0.000000e+00') for wc in self.all_WCs])
        paramcard=param_card_template.format(**wc_dict)
        fo=open('param_card_%s_sm.dat'%(process),'w')
        fo.write(paramcard); fo.close()
        self.param_cards.append('param_card_%s_sm.dat'%(process))


        for i,op in enumerate(self.WCs_per_process[process]): 
            wc_dict = dict( [(wc, '0.000000e+00') for wc in self.all_WCs])
            wc_dict[op]="1.000000e+00"
            paramcard=param_card_template.format(**wc_dict)
            fo=open('param_card_%s_%s_1.dat'%(process, op),'w')
            fo.write(paramcard); fo.close()
            self.param_cards.append('param_card_%s_%s_1.dat'%(process, op))

            wc_dict = dict( [(wc, '0.000000e+00') for wc in self.all_WCs])
            wc_dict[op]="2.000000e+00"
            paramcard=param_card_template.format(**wc_dict)
            fo=open('param_card_%s_%s_2.dat'%(process, op),'w')
            fo.write(paramcard); fo.close()
            self.param_cards.append('param_card_%s_%s_2.dat'%(process, op))
            
            for i2,op2 in enumerate(self.WCs_per_process[process]):
                if i < i2: continue
                wc_dict = dict( [(wc, '0.000000e+00') for wc in self.all_WCs])
                wc_dict[op]="1.000000e+00"
                wc_dict[op2]="1.000000e+00"
                paramcard=param_card_template.format(**wc_dict)
                fo=open('param_card_%s_%s_%s_1.dat'%(process, op, op2),'w')
                fo.write(paramcard); fo.close()
                self.param_cards.append( 'param_card_%s_%s_%s_1.dat'%(process, op, op2) ) 


        for card in self.param_cards:
            dirpath = tempfile.mkdtemp(dir=self.tmpdir)
            self.tmpdirs.append(dirpath)
            print(dirpath)
            shutil.copyfile( path + '/allmatrix2py.so', self.tmpdirs[-1] + '/allmatrix2py.so')
            sys.path[-1] =self.tmpdirs[-1]
            self.mods.append(imp.load_module('allmatrix2py',*imp.find_module('allmatrix2py')))
            del sys.modules['allmatrix2py']
            print 'initializing', card
            self.mods[-1].initialise(card)
        print self.mods
        
        self.pdgOrderSorted = [SortPDGs(x.tolist()) for x in self.mods[-1].get_pdg_order()]
        self.pdgOrder = [x.tolist() for x in self.mods[-1].get_pdg_order()]
        self.all_prefix = [''.join(j).strip().lower() for j in self.mods[-1].get_prefix()]
        self.hel_dict = {}; prefix_set = set(self.all_prefix)
        for prefix in prefix_set:
            if hasattr(self.mods[-1], '%sprocess_nhel' % prefix):
                nhel = getattr(self.mods[-1], '%sprocess_nhel' % prefix).nhel
                self.hel_dict[prefix] = {}
                for i, onehel in enumerate(zip(*nhel)):
                    self.hel_dict[prefix][tuple(onehel)] = i + 1

        

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for card in self.param_cards:
            self.wrappedOutputTree.branch('weight_%s'%(card.split('/')[-1].replace('param_card_','').replace('.','_')),'F')

    def endJob(self):
        for dr in self.tmpdirs:
            shutil.rmtree(dr)

    def analyze(self, event):

        lheParts = [l for l in Collection(event, 'LHEPart')]
        pdgs = [x.pdgId for x in lheParts]
        hel  = [x.spin  for x in lheParts]

        

        p = [ ]
        for part in lheParts:
            if part.status < 0: 
                energy = math.sqrt(part.incomingpz*part.incomingpz+part.mass*part.mass)
                p.append([energy,0.,0.,part.incomingpz])
            else:
                p.append([part.p4().E(), part.p4().Px(), part.p4().Py(), part.p4().Pz()])

        # madgraph pads processes with low multiplicities
        while len(pdgs) < len(self.pdgOrderSorted[0]):
            pdgs.append(0)

        evt_sorted_pdgs = SortPDGs(pdgs)

        try:
            idx = self.pdgOrderSorted.index(evt_sorted_pdgs)
        except ValueError:
            print self.pdgOrderSorted
            print '>> Event with PDGs %s does not match any known process' % pdgs
            return res

        target_pdgs=self.pdgOrder[idx]
        pdgs_withIndices = [(y,x) for x,y in enumerate(pdgs)]
        mapping=[]


        for p1 in target_pdgs:
            toremove=None
            for p2 in pdgs_withIndices:
                if p2[0]==p1:
                    mapping.append( p2[1])
                    toremove=p2
                    break
            if toremove:
                pdgs_withIndices.remove(toremove)
            else:
                raise RuntimeError("It shouldn't be here")

        final_pdgs = []
        final_parts = []
        final_hels = []
        for in_Indx in mapping:
            final_pdgs.append(pdgs[in_Indx])
            if final_pdgs[-1] == 0: continue 
            final_parts.append(p[in_Indx])
            final_hels.append(hel[in_Indx])

        if target_pdgs != final_pdgs:
            raise RuntimeError("Wrong pdgid")

        hel_dict = self.hel_dict[self.all_prefix[idx]]
        t_final_hels = tuple(final_hels)

        if t_final_hels in hel_dict:
            nhel = hel_dict[t_final_hels]
        else:
            print "Available helicities are"
            print hel_dict
            print "tried", t_final_hels
            raise RuntimeError("Helicity configuration not found")
        
        com_final_parts = []


        pboost = [final_parts[0][i] + final_parts[1][i] for i in xrange(4)]

        for part in final_parts:
            com_final_parts.append(zboost(part, pboost))
            

        final_parts_i = invert_momenta(com_final_parts)
        scale2=0
        weights=[]
        for mod in self.mods:
            if 0 in final_pdgs: final_pdgs.remove(0)
            weights.append( mod.smatrixhel( final_pdgs, final_parts_i, event.LHE_AlphaS, scale2, nhel) ) 

        for i, card in enumerate(self.param_cards):
            self.wrappedOutputTree.fillBranch('weight_%s'%(card.split('/')[-1].replace('param_card_','')).replace('.','_'), weights[i]/weights[0])


        return True

eft_TTll = lambda : globalEFTreWeighting('ttll')
eft_TTH  = lambda : globalEFTreWeighting('ttH')
eft_TTTT = lambda : globalEFTreWeighting('tttt')
eft_THQ  = lambda : globalEFTreWeighting('tHq')
eft_TllQ = lambda : globalEFTreWeighting('tllq')
eft_TTln = lambda : globalEFTreWeighting('ttln')
