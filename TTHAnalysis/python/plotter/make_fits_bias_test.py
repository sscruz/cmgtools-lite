import os
import sys
import subprocess

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


vars = ["njets", "lep1_pt", "HT", "jet1_pt"]
GREEN = '\033[0;32m'
BLUE = '\033[0;33m'
NC = '\033[0m'  # No Color

step = sys.argv[1]
for variable in vars:
    print("{BLUE}  * Submitting for variable {variable}{NC}".format(BLUE = BLUE, variable = variable, NC = NC))
    for variation in list(variations.keys()):
        for var in ["up", "dn"]:
            print("{RED}    + Doing fit (step {step}) for {variation}{NC}".format(RED = RED, step = step, variation = variation, NC = NC))
            os.system("python ttW_multilepton/makeDifferentialFits.py cards/bias_test/{variable}/{variation}-{var}/ {variable} 2lss {step} {variation}-{var}".format(var = var, variable = variable, variation = variation, step = step)) 
