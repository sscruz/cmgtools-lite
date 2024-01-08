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

#vars = ["njets", "lep1_pt", "HT", "jet1_pt", "max_eta"]
#years = ["2016", "2016APV", "2017", "2018"]


vars = ["njets", "lep1_pt", "HT", "jet1_pt"]
years =["2016", "2016APV", "2017", "2018"]
for year in years:
        print("{GREEN}>> Submitting for year {year}{NC}".format(GREEN = GREEN, year = year, NC = NC))
        for variable in vars:
            print("{BLUE}  * Submitting for variable {variable}{NC}".format(BLUE = BLUE, variable = variable, NC = NC))
            for variation, _ in variations.items():
                print("{RED}    + Submitting for variation {variation} {NC}".format(RED = RED, variation = variation, NC = NC))
                
                
                
                for var in ["up" , "dn"]:  
                    if not os.path.exists("logs_bias_test/{variable}/{eft}_{var}/".format(eft = variation, var = var, variable = variable)):
                        os.system(" mkdir -p logs_bias_test/{variable}/{eft}_{var}/".format(eft = variation, var = var, variable = variable))
                        os.system(" mkdir -p logs_bias_test/cr4l/{eft}_{var}/".format(eft = variation, var = var, variable = variable))
                        os.system(" mkdir -p logs_bias_test/cr3l/{eft}_{var}/".format(eft = variation, var = var, variable = variable))


                    # ------------------------- Cards for the SR ------------------------- #

                    python_command = "python ttW_multilepton/make_cards_new.py bias_test/{variable}/{variation}-{var} {year} 2lss {variable} ".format(var = var, variable = variable, variation = variation, year = year)

                    cmd = subprocess.check_output(python_command, shell=True, universal_newlines=True)
                    cmd_2l_plusplus = cmd.replace("sbatch -c 16 -p batch", "sbatch -c 16 -p batch -J {eft}_{var}_plusplus -e logs_bias_test/{variable}/{eft}_{var}/log_plusplus.%j.%x.err -o logs_bias_test/{variable}/{eft}_{var}/log_plusplus.%j.%x.out".format(eft = variation, var = var, variable = variable))
                    cmd_2l_plusplus = cmd_2l_plusplus.replace("ttW_2lss_0tau_{variable}_{year}".format(variable = variable, year = year), "ttW_2lss_0tau_{variable}_{year}_positive -E ^plusplus".format(variable = variable, year = year)) # tratra



                    print("{RED}        o SIGNAL REGION {NC}".format(RED = GREEN, variation = variation, NC = NC))                    
                    
                    # Add special asimov configs
                    if variation != "nominal": 
                        additional = " --use-alternative-mca ttW_multilepton/mca-includes/bias-test-mcas/{eft}/mca-2lss-{eft}-{var}.txt".format(eft = variation, var = var)
                        cmd_2l_plusplus = cmd_2l_plusplus.replace("mcc-METchoice-prefiring.txt", "mcc-METchoice-prefiring.txt %s"%additional)
                    
                    cmd_2l_minusminus = cmd_2l_plusplus.replace("plus", "minus") # malamente 
                    cmd_2l_minusminus = cmd_2l_minusminus.replace("positive", "negative") # malamente 

                    print(" {BLUE} Variation: {var} {NC}".format(BLUE = BLUE, var = var, NC = NC))
                    os.system("{cmd}".format(cmd = cmd_2l_plusplus))    
                    os.system("{cmd}".format(cmd = cmd_2l_minusminus))    
                
                    # ------------------------- Cards for the GEN level ------------------------- #
                    python_command_gen = "python ttW_multilepton/make_cards_new.py bias_test/{variable}/{variation}-{var} {year} 2lss {variable} gen ".format(var = var, variable = variable, variation = variation, year = year)
                    cmd_gen = subprocess.check_output(python_command_gen, shell=True, universal_newlines=True)
                    cmd_gen = cmd_gen.replace("sbatch", "sbatch -J {eft}_{var}_gen -e logs_bias_test/{variable}/{eft}_{var}/log_gen.%j.%x.err -o logs_bias_test/{variable}/{eft}_{var}/log_gen.%j.%x.out".format(eft = variation, var = var, variable = variable))
                    print("{RED}        o GEN {NC}".format(RED = GREEN, variation = variation, NC = NC))

                    # Use the specific mca for gen with EFT 
                    if variation != "nominal":
                        cmd_gen = cmd_gen.replace("ttW_multilepton/mca-includes/mca-2lss-sigprompt-gen", "ttW_multilepton/mca-includes/bias-test-mcas/{eft}/mca-2lss-{eft}-{var}-gen".format(var = var, eft = variation))

                    os.system("{cmd}".format(cmd = cmd_gen))

                     
        for variation, _ in variations.items():
            for var in ["up" , "dn"]:  

                # ------------------------- Cards for the CR3L level ------------------------- #
                python_command_cr3l = "python ttW_multilepton/make_cards_new.py bias_test/cr3l/{variation}-{var} {year} cr_3l inclusive ".format(var = var, variable = variable, variation = variation, year = year)

                cmd_cr3l = subprocess.check_output(python_command_cr3l, shell=True, universal_newlines=True)
                cmd_cr3l = cmd_cr3l.replace("sbatch", "sbatch -J {eft}_{var}_cr3l -e logs_bias_test/cr3l/{eft}_{var}/log_cr3l.%j.%x.err -o logs_bias_test/cr3l/{eft}_{var}/log_cr3l.%j.%x.out".format(eft = variation, var = var))
                print("{RED}        o CONTROL REGION (3l) {NC}".format(RED = GREEN, variation = variation, NC = NC))

                if variation != "nominal":
                    additional_cr3l = " --use-alternative-mca ttW_multilepton/mca-includes/bias-test-mcas/{eft}/mca-3l-{eft}-{var}.txt".format(eft = variation, var = var)
                    cmd_cr3l = cmd_cr3l.replace("mcc-METchoice-prefiring.txt", "mcc-METchoice-prefiring.txt %s"%additional_cr3l)
                else:
                    cmd_cr3l = cmd_cr3l
                os.system("{cmd}".format(cmd = cmd_cr3l))    

                # ---- Cards for the CR_4l
                
                
                python_command_cr4l = "python ttW_multilepton/make_cards_new.py bias_test/cr4l/{variation}-{var} {year} cr_4l inclusive ".format(var = var, variable = variable, variation = variation, year = year)
                cmd_cr4l = subprocess.check_output(python_command_cr4l, shell=True, universal_newlines=True)
                cmd_cr4l = cmd_cr4l.replace("sbatch", "sbatch -J {eft}_{var}_cr4l -e logs_bias_test/cr4l/{eft}_{var}/log_cr4l.%j.%x.err -o logs_bias_test/cr4l/{eft}_{var}/log_cr4l.%j.%x.out".format(eft = variation, var = var))
                
                if variation != "nominal":
                    additional_cr4l = " --use-alternative-mca ttW_multilepton/mca-includes/bias-test-mcas/{eft}/mca-4l-{eft}-{var}.txt".format(eft = variation, var = var)
                    cmd_cr4l = cmd_cr4l.replace("mcc-METchoice-prefiring.txt", "mcc-METchoice-prefiring.txt %s"%additional_cr4l)
                print("{RED}        o CONTROL REGION (4l) {NC}".format(RED = GREEN, variation = variation, NC = NC))
                os.system("{cmd}".format(cmd = cmd_cr4l))    
                print("{RED}-------------------{NC}".format(RED = RED, NC = NC))
