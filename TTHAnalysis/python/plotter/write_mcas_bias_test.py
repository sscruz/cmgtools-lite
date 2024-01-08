import os
import sys
import subprocess

nominal_xsec = 0.2357

RED = '\033[0;31m'
GREEN = '\033[0;32m'
BLUE = '\033[0;33m'
NC = '\033[0m'  # No Color

variations = {
    # Variation name    # WC, Term, Term2
    "nominal"  :    [0, 0, 0, "ROOT.kBlue"],
    "eftsm"   :    [0, 0, 0, "ROOT.kBlue"],

    # ----------------------- EFT models
# These are from december 2023
    "cQq18"   :    [1,    15,  20,  "ROOT.kMagenta-9"],
    "cQq83"   :    [1,   210,  230, "ROOT.kCyan"],
    "cpQ3"    :    [5,   120,  135, "ROOT.kCyan"],
    "ctG"     :    [0.3, 253,  275, "ROOT.kOrange-3"],
    "ctW"     :    [1,   171,  189, "ROOT.kRed-9"],
    "ctQ1"    :    [0.3,  55,  65,  "ROOT.kAzure-9"],
    "ctQ8"    :    [0.3,  36,  44,  "ROOT.kSpring+8"],
# These are from november 2023
#    "cQq13"   :    [0.1, 78, 90, "ROOT.kOrange-3"],
#    "cQq83"   :    [1, 210,  230, "ROOT.kCyan"],
#    "cQq11"   :    [0.1, 21, 27, "ROOT.kRed-9"],
#    "cQq18"   :    [0.21, 15, 20, "ROOT.kMagenta-9"],
#    "ctQ1"    :    [0.3, 55, 65, "ROOT.kAzure-9"],
#    "ctQ8"    :    [0.3, 36, 44, "ROOT.kSpring+8"],
#    "cpt"     :    [5, 1, 2, "ROOT.kGray"],
#    "cpQM"    :    [5, 105, 119, "ROOT.kOrange+7"],
}

vars = [""]#"njets", "lep1_pt", "HT", "jet1_pt", "max_eta"]

# Write mcas
outpath = "ttW_multilepton/mca-includes/bias-test-mcas/"

if not os.path.exists(outpath):
    os.system("mkdir -p %s"%outpath)


reference_cr_3l = subprocess.check_output("cat ttW_multilepton/mca-3l-mcdata-frdata-inclusive.txt", shell=True, universal_newlines=True)
reference_cr_4l = subprocess.check_output("cat ttW_multilepton/mca-4l-mcdata-frdata.txt", shell=True, universal_newlines=True)

for eft, variation in variations.items():
    
    eftoutpath = os.path.join(outpath, eft)
    if not os.path.exists(eftoutpath):
        os.system("mkdir -p %s"%eftoutpath)
    # ---- Make the RECO level mcas

    print("{GREEN}>> Creating mca RECO level for EFT {eft} {NC}".format(GREEN = GREEN, eft = eft,  NC = NC))
    coeff = variation[0]
    wc1 = variation[1]
    wc2 = variation[2] 
    color = variation[3]
    
    for var in ["up", "dn"]:
        print("  + Variation: {var}".format(var = var))


        # ------------------------------------ SR 2LSS ------------------------------------ #
        template_reco = """TTW_{eft}_{var}+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="5759.2672466085505/37499",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2016"
TTW_{eft}_{var}+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="5765.8911175108615/37500",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2016APV"
TTW_{eft}_{var}+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="11430.228396718906/74416",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2017"
TTW_{eft}_{var}+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="11485.9609381048/74793",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2018"
"""
        if var == "dn":
            template_reco = template_reco.replace("[0]+", "[0]-")        
            template_reco = template_reco.replace("FillColor", "LineStyle=2, FillColor")
        
        reco_mca = template_reco.format( var = var, nom = nominal_xsec, color = color, eft = eft, coeff = coeff, wc1 = wc1, wc2 = wc2, P = "{P}")        
        print("{GREEN}>> Creating mca RECO level for SR 2LSS with EFT signal {eft} {NC}".format(GREEN = GREEN, eft = eft,  NC = NC))
        fout = open( os.path.join(eftoutpath, "mca-2lss-{eft}-{var}.txt".format(eft = eft, var = var)), "w")
        fout.write(reco_mca)
        fout.close()
        
        
        # ------------------------------------ GEN LEVEL ------------------------------------ #
        template_gen = """TTW_{eft}_{var}_inclusive+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): 1 ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="5759.2672466085505/37499",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2016"
TTW_{eft}_{var}_inclusive+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): 1 ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="5765.8911175108615/37500",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2016APV"
TTW_{eft}_{var}_inclusive+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): 1 ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="11430.228396718906/74416",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2017"
TTW_{eft}_{var}_inclusive+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): 1 ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="11485.9609381048/74793",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2018"
"""
        if var == "dn":
            template_gen = template_gen.replace("[0]+", "[0]-")        
            template_gen = template_gen.replace("FillColor", "LineStyle=2, FillColor")
        
        gen_mca = template_gen.format( var = var, nom = nominal_xsec, color = color, eft = eft, coeff = coeff, wc1 = wc1, wc2 = wc2, P = "{P}")        
        print("{GREEN}>> Creating mca RECO level for SR 2LSS with EFT signal {eft} {NC}".format(GREEN = GREEN, eft = eft,  NC = NC))
        fout = open( os.path.join(eftoutpath, "mca-2lss-{eft}-{var}-gen.txt".format(eft = eft, var = var)), "w")
        fout.write(gen_mca)
        fout.close()
        
        # ------------------------------------ CR 3L ------------------------------------ # 
        template_cr3l = """TTW_{eft}_{var}_inclusive+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && LepGood3_isMatchRightCharge ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="5759.2672466085505/37499",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2016"
TTW_{eft}_{var}_inclusive+  : TTln_EFT : {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && LepGood3_isMatchRightCharge ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="5765.8911175108615/37500",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2016APV"
TTW_{eft}_{var}_inclusive+  : TTln_EFT : {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && LepGood3_isMatchRightCharge ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="11430.228396718906/74416",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2017"
TTW_{eft}_{var}_inclusive+  : TTln_EFT : {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge && LepGood3_isMatchRightCharge ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="11485.9609381048/74793",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2018"
    """.format( var = var, nom = nominal_xsec, color = color, eft = eft, coeff = coeff, wc1 = wc1, wc2 = wc2, P = "{P}")

        if var == "dn":
            template_cr3l = template_cr3l.replace("[0]+", "[0]-")        


        reco_mca_cr3l = template_cr3l.format( var = var, nom = nominal_xsec, color = color, eft = eft, coeff = coeff, wc1 = wc1, wc2 = wc2, P = "{P}")        
        print("{GREEN}>> Creating mca RECO level for CR 3L with EFT signal {eft} {NC}".format(GREEN = GREEN, eft = eft,  NC = NC))
        fout_cr3l = open( os.path.join(eftoutpath, "mca-3l-{eft}-{var}.txt".format(eft = eft, var = var)), "w")
        fout_cr3l.write(reco_mca_cr3l)
        fout_cr3l.close()
        # ------------------------------------ CR 4L ------------------------------------ # 

        template_cr4l = """TTW_{eft}_{var}_inclusive+   : TTln_EFT :   {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_mcMatchId!=0 && LepGood2_mcMatchId!=0 && LepGood3_mcMatchId!=0  && LepGood4_mcMatchId!=0 ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="5759.2672466085505/37499",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2016"
TTW_{eft}_{var}_inclusive+  : TTln_EFT : {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_mcMatchId!=0 && LepGood2_mcMatchId!=0 && LepGood3_mcMatchId!=0  && LepGood4_mcMatchId!=0 ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="5765.8911175108615/37500",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2016APV"
TTW_{eft}_{var}_inclusive+  : TTln_EFT : {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_mcMatchId!=0 && LepGood2_mcMatchId!=0 && LepGood3_mcMatchId!=0  && LepGood4_mcMatchId!=0 ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="11430.228396718906/74416",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2017"
TTW_{eft}_{var}_inclusive+  : TTln_EFT : {nom}*(EFTfitCoefficients[0]+ {coeff}*EFTfitCoefficients[{wc1}] + {coeff}*{coeff}*EFTfitCoefficients[{wc2}]): LepGood1_mcMatchId!=0 && LepGood2_mcMatchId!=0 && LepGood3_mcMatchId!=0  && LepGood4_mcMatchId!=0 ; Label="TTln ({eft}_{var})", FillColor={color}, genSumWeightName="11485.9609381048/74793",  FriendsSimple="{P}/A_ttW_diff_info_extended_25gev/",years= "2018"
    """.format( var = var, nom = nominal_xsec, color = color, eft = eft, coeff = coeff, wc1 = wc1, wc2 = wc2, P = "{P}")
        
        if var == "dn":
            template_cr4l = template_cr4l.replace("[0]+", "[0]-")
             
        reco_mca_cr4l = template_cr4l.format( var = var, nom = nominal_xsec, color = color, eft = eft, coeff = coeff, wc1 = wc1, wc2 = wc2, P = "{P}")        
        print("{GREEN}>> Creating mca RECO level for CR 3L with EFT signal {eft} {NC}".format(GREEN = GREEN, eft = eft,  NC = NC))
        fout_cr4l = open( os.path.join(eftoutpath, "mca-4l-{eft}-{var}.txt".format(eft = eft, var = var)), "w")
        fout_cr4l.write(reco_mca_cr4l)
        fout_cr4l.close()
        
