from differential_variables import all_vars

colorlist= ["ROOT.kMagenta+3","ROOT.kBlue-3","ROOT.kCyan-6","ROOT.kGreen+3","ROOT.kOrange-3","ROOT.kRed+2","ROOT.kOrange+3","ROOT.kAzure+5"]

def do_mca_for_var( OBSERVABLE ):
    binning = eval(all_vars[OBSERVABLE].CATBINS_Gen)
    REGION = all_vars[OBSERVABLE].REGION
    OBSERVABLE_NAME = OBSERVABLE[0]
    
    full_mca_template='''incl_sig : + ; IncludeMca="ttW_multilepton/mca-includes/mca-{REGION}-sigprompt-{OBSERVABLE}.txt"
incl_bkg : + ; IncludeMca="ttW_multilepton/mca-includes/mca-{REGION}-bkgprompt.txt"
incl_convs     : + ; IncludeMca="ttW_multilepton/mca-includes/mca-{REGION}-convs.txt"
incl_datafakes  : + ; IncludeMca="ttW_multilepton/mca-includes/mca-data.txt", FakeRate="ttW_multilepton/fakeRate-{REGION}-frdata.txt", Label="Non-prompt", FillColor=ROOT.kBlack, FillStyle=3005, PostFix='_fakes'
incl_promptsub : + ; IncludeMca="ttW_multilepton/mca-includes/mca-{REGION}-sigprompt-inclusive.txt", FakeRate="ttW_multilepton/fakeRate-{REGION}-frdata.txt", PostFix='_promptsub', AddWeight="-1"
incl_promptsub : + ; IncludeMca="ttW_multilepton/mca-includes/mca-{REGION}-bkgprompt.txt", FakeRate="ttW_multilepton/fakeRate-{REGION}-frdata.txt", PostFix='_promptsub', AddWeight="-1"
incl_dataflips  : + ; IncludeMca="ttW_multilepton/mca-includes/mca-data-forFlips.txt", FakeRate="ttW_multilepton/flipRate-{REGION}-frdata.txt", Label="Charge mis-m.", FillColor=ROOT.kBlack, FillStyle=3006, PostFix='_flips'

incl_data : + ; IncludeMca="ttW_multilepton/mca-includes/mca-data.txt"'''

    # Remove flips in 3l
    if REGION == "3l":
        full_mca_template = full_mca_template.replace("""incl_dataflips  : + ; IncludeMca="ttW_multilepton/mca-includes/mca-data-forFlips.txt", FakeRate="ttW_multilepton/flipRate-{REGION}-frdata.txt", Label="Charge mis-m.", FillColor=ROOT.kBlack, FillStyle=3006, PostFix='_flips'""", "")

    outf1=open("ttW_multilepton/mca-{REGION}-mcdata-frdata-{OBSERVABLE}.txt".format(OBSERVABLE=OBSERVABLE_NAME, REGION=REGION),'w')
    outf1.write( full_mca_template.format(OBSERVABLE=OBSERVABLE_NAME, REGION = REGION).lstrip())
    outf1.close()

    # Template for the signal 
    if REGION == "2lss":
        template='''TTW_{OBSERVABLE}_bin{binno}+     : TTWToLNu_fxfx_withGen : 0.2316 : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && ({FUNCTION_2L} >= {cutlow}) && ({FUNCTION_2L} < {cuthigh}) && (nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[0]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1) ; FillColor={color}   , Label="{cutlow} <= ttW {OBSERVABLE} < {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended_25gev_fixed/"
TTW_{OBSERVABLE}_bin{binno}+     : TTWJetsToLNu_EWK_5f_NLO_withGen : 0.0113 : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && ({FUNCTION_2L} >= {cutlow}) && ({FUNCTION_2L} < {cuthigh}) && (nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[0]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1) ; FillColor={color}   , Label="{cutlow} <= ttW {OBSERVABLE}  < {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended_25gev_fixed/"\n'''
        
    elif REGION == "3l":
        template='''TTW_{OBSERVABLE}_bin{binno}+     : TTWToLNu_fxfx_withGen : 0.2316 : LepGood1_mcMatchId!=0 && LepGood2_mcMatchId!=0 && LepGood3_mcMatchId!=0 && ({FUNCTION_2L} >= {cutlow}) && ({FUNCTION_2L} < {cuthigh}) && (nDressSelLep > 2) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  15 && GenDressedLepton_pt[iDressSelLep[2]] > 10) && (nDressSelJet >= 2) && (nDressBSelJet >=1) ; FillColor={color}  , Label="{cutlow} <= ttW {OBSERVABLE} < {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended_25gev_fixed/"
TTW_{OBSERVABLE}_bin{binno}+     : TTWJetsToLNu_EWK_5f_NLO_withGen : 0.0113 : LepGood1_mcMatchId!=0 && LepGood2_mcMatchId!=0 && LepGood3_mcMatchId!=0 &&  ({FUNCTION_2L} >= {cutlow}) && ({FUNCTION_2L} < {cuthigh}) && (nDressSelLep > 2) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  15 && GenDressedLepton_pt[iDressSelLep[2]] >  10) && (nDressSelJet >= 2) && (nDressBSelJet >=1) ; FillColor={color}   , Label="{cutlow} <= ttW {OBSERVABLE}  < {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended_25gev_fixed/"\n'''
    
      

    signal_mca=""
    print(binning[1:-1])
    for i,(binlow,binhigh) in enumerate(zip(binning, binning[1:-1])):
        signal_mca += template.format(binno=i, cutlow=binlow, color= colorlist[i], cuthigh=binhigh, OBSERVABLE=OBSERVABLE_NAME, FUNCTION_2L=all_vars[OBSERVABLE].FUNCTION_2L)
    signal_mca+='''TTW_{OBSERVABLE}_bin{binno}+     : TTWToLNu_fxfx_withGen : 0.2316 : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && ({FUNCTION_2L} > {cuthigh}) && (nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[0]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1) ; FillColor={color}   , Label="ttW {OBSERVABLE}  > {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended_25gev_fixed/"
TTW_{OBSERVABLE}_bin{binno}+     : TTWJetsToLNu_EWK_5f_NLO_withGen : 0.0113 : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && ({FUNCTION_2L} > {cuthigh}) && (nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[0]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1) ; FillColor={color}   , Label=" ttW {OBSERVABLE}  > {cuthigh}", FillStyle=3022,  FriendsSimple="{{P}}/A_ttW_diff_info_extended_25gev_fixed/"\n'''.format(binno=i+1, cutlow=binlow, color= colorlist[i+1], cuthigh=binning[-2], OBSERVABLE=OBSERVABLE_NAME, FUNCTION_2L=all_vars[OBSERVABLE].FUNCTION_2L)

    if REGION == "2lss":
        signal_mca+='''TTW_ooa+     : TTWToLNu_fxfx_withGen :0.2316: LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && !((nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[0]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1)) ;  FillColor=ROOT.kGreen-5, Label="ttW (<2 leps)", FriendsSimple="{P}/A_ttW_diff_info_extended_25gev_fixed/"  
TTW_ooa+     : TTWJetsToLNu_EWK_5f_NLO_withGen : 0.0113 : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && !((nDressSelLep > 1) && (GenDressedLepton_pdgId[iDressSelLep[0]]*GenDressedLepton_pdgId[iDressSelLep[1]]>0) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  20) && (nDressSelJet >= 3) && (nDressBSelJet >=1)) ; FillColor=ROOT.kGreen-5, Label="ttW (<2 leps)", FriendsSimple="{P}/A_ttW_diff_info_extended_25gev_fixed/" \n'''
    
    elif REGION == "3l":
        signal_mca+='''TTW_ooa+     : TTWToLNu_fxfx_withGen :0.2316: LepGood1_mcMatchId!=0 && LepGood2_mcMatchId!=0 && LepGood3_mcMatchId!=0 && !((nDressSelLep > 2) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  15 && GenDressedLepton_pt[iDressSelLep[2]] >  10) && (nDressSelJet >= 2) && (nDressBSelJet >=1)) ;  FillColor=ROOT.kGreen-5, Label="ttW (<2 leps)", FriendsSimple="{P}/A_ttW_diff_info_extended_25gev_fixed/"  
TTW_ooa+     : TTWJetsToLNu_EWK_5f_NLO_withGen : 0.0113 : LepGood1_mcMatchId!=0 && LepGood2_mcMatchId!=0 && LepGood3_mcMatchId!=0 && !((nDressSelLep > 2) && (GenDressedLepton_pt[iDressSelLep[0]] > 25 && GenDressedLepton_pt[iDressSelLep[1]] >  15 && GenDressedLepton_pt[iDressSelLep[2]] > 10) && (nDressSelJet >= 2) && (nDressBSelJet >=1)) ; FillColor=ROOT.kGreen-5, Label="ttW (<2 leps)", FriendsSimple="{P}/A_ttW_diff_info_extended_25gev_fixed/"\n'''

    outf2=open("ttW_multilepton/mca-includes/mca-{REGION}-sigprompt-{OBSERVABLE}.txt".format(OBSERVABLE=OBSERVABLE_NAME, REGION=REGION),'w')
    outf2.write( signal_mca.lstrip() )
    outf2.close()


for obs in all_vars:
        do_mca_for_var(obs)
