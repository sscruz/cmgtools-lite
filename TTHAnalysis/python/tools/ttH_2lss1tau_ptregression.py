from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 

import h5py

from copy import deepcopy
import ROOT
import numpy as np




class ttH_2lss1tau_ptregression(Module):

    def __init__(self, tesYear = "2018", variations=[], doSystJEC=True):
        from keras.models import load_model # I acknowledge this is horrible, but it's currently necessary until the global pt_dnns are streamlined
        import tensorflow as tf # I acknowledge this is horrible, but it's currently necessary until the global pt_dnns are streamlined
        def loss_MAEDeltaVar(y_true, y_pred):
            y_true = tf.cast(y_true,tf.float32)
            y_pred = tf.cast(y_pred,tf.float32)
            y_true_mean = tf.reduce_mean(y_true)
            y_pred_mean = tf.reduce_mean(y_pred)
            base = tf.reduce_mean(abs(y_true-y_pred))
            var_true = tf.reduce_mean((y_true-y_true_mean)**2)
            var_pred = tf.reduce_mean((y_pred-y_pred_mean)**2)
            var_diff = abs(var_true - var_pred)
            val = base*var_diff
            return val
        def loss_MSEDeltaVar(y_true, y_pred):
            y_true = tf.cast(y_true,tf.float32)
            y_pred = tf.cast(y_pred,tf.float32)
            y_true_mean = tf.reduce_mean(y_true)
            y_pred_mean = tf.reduce_mean(y_pred)
            base = tf.reduce_mean((y_true-y_pred)**2)
            var_true = tf.reduce_mean((y_true-y_true_mean)**2)
            var_pred = tf.reduce_mean((y_pred-y_pred_mean)**2)
            var_diff = abs(var_true - var_pred)
            val = base*var_diff
            return val

        self.systsJEC = {0:"",\
                         1:"_jesTotalCorrUp"  , -1:"_jesTotalCorrDown",\
                         2:"_jesTotalUnCorrUp", -2: "_jesTotalUnCorrDown",\
                         3:"_jerUp", -3: "_jerDown",\
                     } if doSystJEC else {0:""}
        if len(variations): 
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
        self._MVAs=[]
        self.outVars=[]
        self.model_regression = load_model(os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/regressionMVA/dnn_trained_2lss1tau_UL.h5"), custom_objects={'loss_MSEDeltaVar': loss_MSEDeltaVar})
        print("/home/ucl/cp3/atalier/final_tth/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/data/TauIDSFs/TauES_dm_DeepTau2017v2p1VSjet_UL{}.root".format(tesYear))
        self.rootFile = "/home/ucl/cp3/atalier/final_tth/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/data/TauIDSFs/TauES_dm_DeepTau2017v2p1VSjet_UL{}.root".format(tesYear)
        for var in self.systsJEC:
            self.outVars.extend( ['ttH_higgs_pt_2lss1tau%s_'%self.systsJEC[var] ])
        self.outVars.extend( ['HTXS_Higgs_pt'] )
    def applyTES(self, ev):
        file = ROOT.TFile(self.rootFile)
        hist = file.Get('tes')
        return hist.GetBinContent(hist.GetXaxis().FindBin(ev.TauSel_Recl_decayMode[int(ev.Tau_tight2lss1tau_idx)]))
    def getVarForVar(self, var, ev):
        return { 
            'SelJet1_pt'            : getattr(ev,'JetSel_Recl_pt%s'%var)[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet1_eta'           : ev.JetSel_Recl_eta[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet1_phi'           : ev.JetSel_Recl_phi[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet1_isFromHadTop'  : getattr(ev,'jetobjects')[0].isFromHadTop if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet2_isFromHadTop'  : getattr(ev,'jetobjects')[1].isFromHadTop if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
            'SelJet1_btagDeepFlavB' : ev.JetSel_Recl_btagDeepFlavB[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet2_pt'            : getattr(ev,'JetSel_Recl_pt%s'%var)[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
            'SelJet2_eta'           : ev.JetSel_Recl_eta[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
            'SelJet2_phi'           : ev.JetSel_Recl_phi[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
            'SelJet2_btagDeepFlavB' : ev.JetSel_Recl_btagDeepFlavB[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
            'Lep1_pt'               : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])],
            'Lep2_pt'               : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
            'Lep1_eta'              : ev.LepGood_eta[int(ev.iLepFO_Recl[0])],
            'Lep2_eta'              : ev.LepGood_eta[int(ev.iLepFO_Recl[1])],
            'Lep1_phi'              : ev.LepGood_phi[int(ev.iLepFO_Recl[0])],
            'Lep2_phi'              : ev.LepGood_phi[int(ev.iLepFO_Recl[1])],
            'nSelJets'              : getattr(ev,'nJet25%s_Recl'%var),
            'met'                   : getattr(ev,'MET_pt'),#%s'%var), #if isData else getattr(ev,'MET_T1_pt'),
#            'met'                   : getattr(ev,'MET_T1_pt%s'%var) if ev.year != 2017 else getattr(ev,'METFixEE2017_pt%s'%var),
            'HTT_score'             : getattr(ev,'BDThttTT_eventReco_mvaValue%s'%(var)) if getattr(ev,'BDThttTT_eventReco_mvaValue%s'%(var)) > 0 else 0,
            'visHiggs_pt'           : ev.visHiggs_pt,
            'visHiggs_eta'          : ev.visHiggs_eta,
            'mT_lep2'               : getattr(ev,'MT_met_lep2%s'%var),
            'mT_lep1'               : getattr(ev,'MT_met_lep1%s'%var),
            'Hj_tagger_hadTop'      : getattr(ev,'BDThttTT_eventReco_Hj_score%s'%(var)) if getattr(ev,'BDThttTT_eventReco_Hj_score%s'%(var)) > 0 else 0 ,
            'avg_dr_jet'            : getattr(ev,'avg_dr_jet%s'%var) if  getattr(ev,'avg_dr_jet%s'%var) > 0 else -9,
            'mTTH_2lss1tau'         : ev.mTTH_2lss1tau,
            'Tau_pt'                : getattr(ev,'thetau').pt*self.applyTES(ev)  if getattr(ev,'thetau') else 0,
            'Tau_eta'               : getattr(ev,'thetau').eta if getattr(ev,'thetau') else 0,
            'Tau_phi'               : getattr(ev,'thetau').phi if getattr(ev,'thetau') else 0,
#            'Tau_pt'                : getattr(ev,'thetau').pt*hist.GetBinContent(hist.GetXaxis().FindBin(getattr(ev,'thedm'))  if getattr(ev,'thetau') else 0,
#            'Tau_eta'               : getattr(ev,'thetau').eta*hist.GetBinContent(hist.GetXaxis().FindBin(getattr(ev,'thedm')) if getattr(ev,'thetau') else 0,
#            'Tau_phi'               : getattr(ev,'thetau').phi*hist.GetBinContent(hist.GetXaxis().FindBin(getattr(ev,'thedm')) if getattr(ev,'thetau') else 0,

        }


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        declareOutput(self, wrappedOutputTree, self.outVars)

    def analyze(self,event):
        varorder=['Lep1_pt','Lep2_pt','Lep1_eta','Lep2_eta','Lep1_phi','Lep2_phi','nSelJets','SelJet1_pt','SelJet2_pt','SelJet1_eta','SelJet2_eta','SelJet1_phi','SelJet2_phi','SelJet1_isFromHadTop','SelJet2_isFromHadTop','SelJet1_btagDeepFlavB','SelJet2_btagDeepFlavB','met','HTT_score','visHiggs_pt','visHiggs_eta','mT_lep2','mT_lep1','Hj_tagger_hadTop','avg_dr_jet','mTTH_2lss1tau','Tau_pt','Tau_eta','Tau_phi']

        taus = [ t for t in Collection(event,'TauSel_Recl')]
        #dms = [ d for d in Collection(event,'TauSel_Recl_decayMode')]
        #print("ciao ", taus)
        setattr(event , 'thetau', taus[int(event.Tau_tight2lss1tau_idx)] if event.Tau_tight2lss1tau_idx > -1 else None)
#        setattr(event , 'thedm', dms[int(event.Tau_tight2lss1tau_idx)] if event.Tau_tight2lss1tau_idx > -1 else None)
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        jets = [j for j in Collection(event,"JetSel_Recl")]

        try:
            gen = leps[0].genPartFlav
            isData = False
        except:
            isData = True

        if(isData): self.systsJEC = {0:""}

        if event.thetau and len(leps)>1:
            higgsLepton = leps[0] if deltaR(event.thetau,leps[0]) < deltaR(event.thetau,leps[1]) else leps[1]
            visHiggs = higgsLepton.p4() + event.thetau.p4()*self.applyTES(event)


            tthSystem = higgsLepton.p4() + event.thetau.p4()*self.applyTES(event)
            for j in [j for j in jets if j.pt >= 25][:4]:
                tthSystem+=j.p4()
            vmet=ROOT.TLorentzVector()
            if isData:
                vmet.SetPtEtaPhiM(event.MET_pt, 0, event.MET_phi, 0)
            else:
                vmet.SetPtEtaPhiM(event.MET_T1_pt, 0, event.MET_phi, 0)
            tthSystem+=vmet


            setattr(event, 'visHiggs_pt' , visHiggs.Pt())
            setattr(event, 'visHiggs_eta', visHiggs.Eta())
            setattr(event, 'mTTH_2lss1tau', tthSystem.M())
        else:
            setattr(event, 'visHiggs_pt' , 0)
            setattr(event, 'visHiggs_eta', 0)
            setattr(event, 'mTTH_2lss1tau', 0)
        jets = [j for j in Collection(event,"JetSel_Recl")]
        for j in jets: 
            setattr(j, 'isFromHadTop', jets.index(j) in [int(event.BDThttTT_eventReco_iJetSel1), int(event.BDThttTT_eventReco_iJetSel2), int(event.BDThttTT_eventReco_iJetSel3)])
        setattr(event, 'jetobjects', jets)
        ret=[]
        for var in self.systsJEC:
            if len(leps) < 2:
                dnn_pred = -99
            else:
                thevars = [[self.getVarForVar(self.systsJEC[var],event)[i]] for i in varorder]
                # MCTruth was scaled from [x_min,x_max] to [-0.8,0.8]. This undoes the transformation
#                x_min = 0.26197815
#                x_max = 1275.8125
#                dnn_pred_scaled = self.model_regression.predict(np.transpose(np.array(thevars)))
#                dnn_pred = dnn_pred_scaled * (x_max - x_min)/1.6 + (x_max + x_min)/2.0
                dnn_pred = self.model_regression.predict(np.transpose(np.array(thevars)))

            self.out.fillBranch('ttH_higgs_pt_2lss1tau%s_'%self.systsJEC[var], dnn_pred)
        self.out.fillBranch('HTXS_Higgs_pt', getattr(event,"HTXS_Higgs_pt") if(isData == False) else -99)

        return True


