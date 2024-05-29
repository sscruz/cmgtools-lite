class Observable:
    def __init__(self, FUNCTION_2L, FUNCTION_2Lreco,  CATBINS, CATBINS_Gen, REGION = "2lss"):
        self.FUNCTION_2L=FUNCTION_2L
        self.FUNCTION_2Lreco=FUNCTION_2Lreco
        self.CATBINS=CATBINS
        self.CATBINS_Gen=CATBINS_Gen
        self.REGION = REGION



all_vars={}

for REGION in ["2lss", "3l"]:
    for OBSERVABLE in ["njets","njets_7bins","nbjets_medium","nbjets","lep1_pt","lep2_pt", "dR_ll","lep1_eta", "lep2_eta", "max_eta","jet1_pt", "jet2_pt", "jet1_eta", "jet2_eta", "bMediumLeadingJet_pt", "bMediumLeadingJet_eta", "bLooseLeadingJet_pt", "bLooseLeadingJet_eta", "mll", "sum_2lss_pt", "deta_llss","dR_lbmedium","dR_lbloose","mindr_lep1_jet25","HT","m3l","pt3l"]:
        if OBSERVABLE == "njets":
            FUNCTION_2L="nDressSelJet"
            FUNCTION_2Lreco="nJet25"
            if REGION == "2lss":
                CATBINS      ="[2.5,3.5,4.5,5.5]"
                CATBINS_Gen  = CATBINS
            elif REGION == "3l":
                CATBINS      ="[2.5,3.5,4.5,5.5]"
                CATBINS_Gen  = CATBINS

        if OBSERVABLE == "njets_7bins":
            FUNCTION_2L="nDressSelJet"
            FUNCTION_2Lreco="nJet25"
            if REGION == "2lss":
                CATBINS      ="[2.5,3.5,4.5,5.5,6.5,7.5]"
                CATBINS_Gen  = CATBINS
            elif REGION == "3l":
                CATBINS      ="[2.5,3.5,4.5,5.5,6.5,7.5]"
                CATBINS_Gen  = CATBINS
                
                
        elif OBSERVABLE == "nbjets_medium":
            FUNCTION_2L="nDressBSelJet"
            FUNCTION_2Lreco="nBJetLoose25"
            if REGION == "2lss":
                CATBINS    ="[0.5,1.5,2.5,3.5]"
                CATBINS_Gen  = CATBINS
            elif REGION == "3l":
                CATBINS    ="[0.5,1.5,2.5,3.5]"

                CATBINS_Gen  = CATBINS
        elif OBSERVABLE == "nbjets":
            FUNCTION_2L="nDressBSelJet"
            FUNCTION_2Lreco="nBJetLoose25"
            if REGION == "2lss":
                CATBINS    ="[1.5,2.5,3.5]"
                CATBINS_Gen  = CATBINS
            elif REGION == "3l":
                CATBINS    ="[1.5,2.5,3.5]"
                CATBINS_Gen  = CATBINS
                
        elif OBSERVABLE == "lep1_pt":
            FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[0]]"
            FUNCTION_2Lreco="LepGood1_conePt"
            if REGION == "2lss":
                CATBINS    = "[25, 37, 50, 62, 75, 97, 120, 160, 200]"
                CATBINS_Gen  ="[25, 50, 75, 120, 200]"
            elif REGION == "3l":
                CATBINS    = "[25,50,70,85,100,120,150,200,300]"
                CATBINS_Gen  ="[25,70,100,150,300]" 
                               
        elif OBSERVABLE == "lep2_pt":
            FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[1]]"
            FUNCTION_2Lreco="LepGood2_conePt"
            if REGION == "2lss":
                CATBINS    ="[15, 22, 30, 40, 50, 75, 100]"
                CATBINS_Gen    ="[15, 30, 50, 100]"
            elif REGION == "3l":
                CATBINS    ="[15,30,45,70,100,200]"
                CATBINS_Gen    ="[15,45,100,200]"
        
        elif OBSERVABLE == "sum_2lss_pt":
            FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[0]]+GenDressedLepton_pt[iDressSelLep[1]]"
            FUNCTION_2Lreco="LepGood1_conePt+LepGood2_conePt"
            if REGION == "2lss":
                CATBINS    = "[0.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0]"
                CATBINS_Gen  ="[0.0, 100.0, 200.0, 300.0, 400.0]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "mll":
            FUNCTION_2L="mass_2(GenDressedLepton_pt[iDressSelLep[0]], GenDressedLepton_eta[iDressSelLep[0]], GenDressedLepton_phi[iDressSelLep[0]], 0, GenDressedLepton_pt[iDressSelLep[1]], GenDressedLepton_eta[iDressSelLep[1]], GenDressedLepton_phi[iDressSelLep[1]], 0)"
            FUNCTION_2Lreco="mass_2(LepGood1_conePt, LepGood1_eta, LepGood1_phi, 0, LepGood2_conePt, LepGood2_eta, LepGood2_phi, 0)"
            if REGION == "2lss":
                CATBINS    = "[0.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0]"
                CATBINS_Gen  ="[0.0, 100.0, 200.0, 300.0, 400.0]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "dR_ll":
            FUNCTION_2L="deltaR(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_phi[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]],GenDressedLepton_phi[iDressSelLep[1]])"
            FUNCTION_2Lreco="deltaR(LepGood1_eta,LepGood1_phi,LepGood2_eta,LepGood2_phi)"
            if REGION == "2lss":
                CATBINS    = "[0.0,0.8,1.6,2.1,2.9,3.3,4.1,5.0]"
                CATBINS_Gen    ="[0, 1.6, 2.5, 3.3, 5]"
            elif REGION == "3l":
                continue # Not implemented
            
        elif OBSERVABLE == "lep1_eta":
            FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]])"
            FUNCTION_2Lreco="abs(LepGood1_eta)"
            if REGION == "2lss":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"
            elif REGION == "3l":
                CATBINS    ="[0.0,0.2,0.4,0.6,0.8,1.0,1.3,1.8,2.5]"
                CATBINS_Gen    ="[0.0,0.4,0.8,1.3,2.5]"
        
        elif OBSERVABLE == "lep2_eta":
            FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[1]])"
            FUNCTION_2Lreco="abs(LepGood2_eta)"
            if REGION == "2lss":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"
            elif REGION == "3l":
                CATBINS    ="[0.0,0.2,0.4,0.6,0.8,1.0,1.3,1.8,2.5]"
                CATBINS_Gen    ="[0.0,0.4,0.8,1.3,2.5]"
                                
        elif OBSERVABLE == "max_eta":
            FUNCTION_2L="max(abs(GenDressedLepton_eta[iDressSelLep[0]]),abs(GenDressedLepton_eta[iDressSelLep[1]]))"
            FUNCTION_2Lreco="max(abs(LepGood1_eta),abs(LepGood2_eta))"
            if REGION == "2lss":
                CATBINS    ="[0, 0.5, 1.0, 1.25, 1.5, 1.75, 2, 2.25, 2.5]"
                CATBINS_Gen    ="[0, 1.0, 1.5, 2, 2.5]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "bLooseLeadingJet_pt":
            FUNCTION_2L="GenJet_pt[iDressSelBJet[0]]"
            FUNCTION_2Lreco="bLooseLeadingJet_pt"
            if REGION == "2lss":
                CATBINS        ="[25, 55, 85, 118.0, 150, 175.0, 200]"
                CATBINS_Gen    ="[25.0, 85.0, 150.0, 200.0]"
            elif REGION == "3l":
                CATBINS        ="[25,95,150,200,300,450]"
                CATBINS_Gen    ="[25,150,300,450]"
 
        elif OBSERVABLE == "bMediumLeadingJet_pt":
            FUNCTION_2L="GenJet_pt[iDressSelBJet[0]]"
            FUNCTION_2Lreco="bMediumLeadingJet_pt"
            if REGION == "2lss":
                CATBINS        ="[25, 55, 85, 118.0, 150, 175.0, 200]"
                CATBINS_Gen    ="[25.0, 85.0, 150.0, 200.0]"
            elif REGION == "3l":
                CATBINS        ="[25,95,150,200,300,450]"
                CATBINS_Gen    ="[25,150,300,450]"       

        elif OBSERVABLE == "bMediumLeadingJet_eta":
            FUNCTION_2L="abs(GenJet_eta[iDressSelBJet[0]])"
            FUNCTION_2Lreco="bMediumLeadingJet_eta"
            if REGION == "2lss":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"
            elif REGION == "3l":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"

        elif OBSERVABLE == "bLooseLeadingJet_eta":
            FUNCTION_2L="abs(GenJet_eta[iDressSelBJet[0]])"
            FUNCTION_2Lreco="bLooseLeadingJet_eta"
            if REGION == "2lss":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"
            elif REGION == "3l":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"

        elif OBSERVABLE == "jet1_pt":
            FUNCTION_2L="GenJet_pt[iDressSelJet[0]]"
            FUNCTION_2Lreco="JetSel_Recl_pt[0]"
            if REGION == "2lss":
                CATBINS        ="[25, 62, 100, 140, 180, 240, 300]"
                CATBINS_Gen    ="[25, 100, 180, 300]"
            elif REGION == "3l":
                CATBINS        ="[25,95,150,200,300,450]"
                CATBINS_Gen    ="[25,150,300,450]"
        
        elif OBSERVABLE == "jet2_pt":
            FUNCTION_2L="GenJet_pt[iDressSelJet[1]]"
            FUNCTION_2Lreco="JetSel_Recl_pt[1]"
            if REGION == "2lss":
                CATBINS        ="[25, 62, 100, 140, 180, 240, 300]"
                CATBINS_Gen    ="[25, 100, 180, 300]"
            elif REGION == "3l":
                CATBINS        ="[25,95,150,200,300,450]"
                CATBINS_Gen    ="[25,150,300,450]"
        
        elif OBSERVABLE == "jet1_eta":
            FUNCTION_2L="abs(GenJet_eta[iDressSelJet[0]])"
            FUNCTION_2Lreco="abs(JetSel_Recl_eta[0])"
            if REGION == "2lss":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"
            elif REGION == "3l":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"

        elif OBSERVABLE == "jet2_eta":
            FUNCTION_2L="abs(GenJet_eta[iDressSelJet[1]])"
            FUNCTION_2Lreco="abs(JetSel_Recl_eta[1])"
            if REGION == "2lss":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"
            elif REGION == "3l":
                CATBINS    ="[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]"
                CATBINS_Gen    ="[0, 0.5, 1.0, 1.5, 2.5]"

        elif OBSERVABLE == "deta_llss":
            FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]]-GenDressedLepton_eta[iDressSelLep[1]])"
            FUNCTION_2Lreco="abs(LepGood1_eta-LepGood2_eta)"
            if REGION == "2lss":
                CATBINS    ="[0,0.25,0.5,0.75,1.10,1.5,2.1,2.5]"
                CATBINS_Gen    ="[0,0.5,1.10,2.1,2.5]"
            elif REGION == "3l":
                continue # Not implemented
       
        elif OBSERVABLE == "dR_lbmedium":
            FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
            FUNCTION_2Lreco="dR_lbmedium"
            if REGION == "2lss":
                CATBINS    ="[0, 0.5,1.0,1.25, 1.5,1.75, 2.0,2.25, 2.5,2.75, 3.0,3.25,3.5,3.75,4.0]"
                CATBINS_Gen    ="[0, 1.0, 1.5, 2.0, 2.5, 3.0,3.5,4.0]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "dR_lbloose":
            FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
            FUNCTION_2Lreco="dR_lbloose"
            if REGION == "2lss":
                CATBINS    ="[0, 0.5,1.0,1.25, 1.5,1.75, 2.0,2.25, 2.5,2.75, 3.0,3.25,3.5,3.75,4.0]"
                CATBINS_Gen    ="[0, 1.0, 1.5, 2.0, 2.5, 3.0,3.5,4.0]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "mindr_lep1_jet25":
            FUNCTION_2L="mindr_DressSelLep_JetDressSel"
            FUNCTION_2Lreco="mindr_lep1_jet25"
            if REGION == "2lss":
                CATBINS    ="[0, 0.5, 1, 1.25, 1.5, 1.75, 2, 2.5, 3]"
                CATBINS_Gen    ="[0, 1, 1.5, 2, 3]"
            elif REGION == "3l":
                continue # Not implemented

        elif OBSERVABLE == "HT":
            FUNCTION_2L="Gen_HT"
            FUNCTION_2Lreco="htJet25j_Recl"
            if REGION == "2lss":
                CATBINS    ="[0, 125, 250, 325, 400, 500, 600, 800, 1000]"
                #CATBINS_Gen    ="[0.0,200,300.,450,600.,2000.]"
                CATBINS_Gen    ="[0, 250, 400, 600, 1000]"

            elif REGION == "3l":
                CATBINS    ="[0.0,100,200,250,300.,375,450,525,600.,1400.,2000.]"
                CATBINS_Gen    ="[0.0,200,300.,450,600.,2000.]"
        
        elif OBSERVABLE == "m3l":
            FUNCTION_2L="mass_3_cheap(GenDressedLepton_pt[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_pt[iDressSelLep[1]],GenDressedLepton_eta[iDressSelLep[1]],GenDressedLepton_phi[iDressSelLep[1]]-GenDressedLepton_phi[iDressSelLep[0]],GenDressedLepton_pt[iDressSelLep[2]],GenDressedLepton_eta[iDressSelLep[2]],GenDressedLepton_phi[iDressSelLep[2]]-GenDressedLepton_phi[iDressSelLep[0]])"
            FUNCTION_2Lreco="mass_3_cheap(LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta,LepGood2_phi-LepGood1_phi,LepGood3_pt,LepGood3_eta,LepGood3_phi-LepGood1_phi)"
            if REGION == "2lss":
                continue # Not implemented
            elif REGION == "3l":
                CATBINS    ="[0., 50., 150., 250., 350., 600.]"
                
        elif OBSERVABLE == "pt3l":
            FUNCTION_2L="(GenDressedLepton_pt[iDressSelLep[0]] + GenDressedLepton_pt[iDressSelLep[1]] + GenDressedLepton_pt[iDressSelLep[2]])"
            FUNCTION_2Lreco="LepGood1_pt+LepGood2_pt+LepGood3_pt"
            if REGION == "2lss":
                continue # Not implemented
            elif REGION == "3l":
                CATBINS    ="[0.0, 100,150.,200., 250.,300 ,350.,450. ,800.]"
                CATBINS_Gen    ="[0.0, 150., 250., 350., 800.]"
        
        all_vars[(OBSERVABLE,REGION)]=Observable(FUNCTION_2L, FUNCTION_2Lreco, CATBINS, CATBINS_Gen, REGION)

