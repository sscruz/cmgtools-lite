import os, sys, re
from differential_variables import all_vars
nCores=16


if 'psi' in os.environ['HOSTNAME']:       
    ORIGIN="/pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoTrees_UL_v2_060422_newfts_skim2lss"; 
    queue ="standard"
elif 'fanae' in os.environ['HOSTNAME']:
    ORIGIN     = "/lustrefs/hdd_pool_dir/nanoAODv9/ttH_differential/NanoTrees_UL_v2_060422_skim2lss_newfts/"
    queue ="batch"
elif 'gae' in os.environ['HOSTNAME']: 
    ORIGIN     = "/lustrefs/hdd_pool_dir/nanoAODv9/ttH_differential/NanoTrees_UL_v2_060422_skim2lss_newfts/"
    queue ="batch"

else: 
    raise RuntimeError("You need ntuples to run the analysis :)")

#submit = '{command}' 
submit = '''sbatch -c %d -p %s  --wrap '{command}' '''%(nCores, queue)

if len(sys.argv) < 4: 
    print('Sytaxis is %s [outputdir] [year] [region] [observable] [other]'%sys.argv[0])
    raise RuntimeError 

OUTNAME=sys.argv[1]
YEAR=sys.argv[2]
REGION=sys.argv[3]
OBSERVABLE=sys.argv[4]
OTHER=sys.argv[5:] if len(sys.argv) > 5 else ''

if   YEAR == '2016'   : LUMI="16.8"
elif   YEAR == '2016APV': LUMI="19.5"
elif YEAR in '2017': LUMI="41.48"
elif YEAR in '2018': LUMI="59.83"
else:
    raise RuntimeError("Wrong year %s"%YEAR)


#print "Normalizing to {LUMI}/fb".format(LUMI=LUMI);
OPTIONS=" --tree NanoAOD  -j {J} -l {LUMI}  --s2v -f --WA prescaleFromSkim --split-factor=-1 ".format(LUMI=LUMI,J=nCores)
os.system("test -d cards/{OUTNAME} || mkdir -p cards/{OUTNAME}".format(OUTNAME=OUTNAME))
OPTIONS="{OPTIONS} --od cards/{OUTNAME} ".format(OPTIONS=OPTIONS, OUTNAME=OUTNAME)
if "gen" in OTHER:
   OPTIONS = OPTIONS.replace("--WA prescaleFromSkim","")
   ltext = "-l {LUMI}".format(LUMI=LUMI)



T2L="-P {ORIGIN}/{YEAR} --FMCs {{P}}/0_jmeUnc_merged  --FMCs {{P}}/2_btag_SFs_WPfixed_25GeV// --FMCs {{P}}/2_scalefactors_lep/ --Fs {{P}}/4_evtVars_matteoflavor --Fs {{P}}/6_ttWforlepton --Fs {{P}}/7_Vars_forttWDiff_25 --FMCs {{P}}/1_recl_allvars_withmatteoflavor --FDs {{P}}/1_recl  --xf GGHZZ4L_new,qqHZZ4L,tWll,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,TGJets_lep,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,ZGTo2LG,GluGluToHHTo4V,TTTW ".format(ORIGIN=ORIGIN, YEAR=YEAR)


if "gen" in OTHER:
   T2L= "-P {ORIGIN}/NanoTrees_UL_v2_gennoskim_190923/{YEAR} ".format(ORIGIN = re.sub("NanoTrees_UL_v2_060422_.*","",ORIGIN), YEAR=YEAR)


T3L=T2L
T4L=T2L

#SYSTS="--unc ttW_multilepton/systsUnc.txt --amc --xu CMS_ttWl_WZ_lnU,CMS_ttWl_ZZ_lnU,QCDscale_ttW,CMS_ttHl_TTW_lnU,CMS_ttHl_TTZ_lnU"
SYSTS="--unc ttW_multilepton/systsUnc.txt --amc --xu QCDscale_ttW,CMS_ttHl_TTW_lnU"
MCAOPTION=""
MCAOPTION=""
ASIMOV="--asimov signal"
SCRIPT= "makeShapeCardsNew.py"
PROMPTSUB="--plotgroup data_fakes+=.*_promptsub"

print("other:",OTHER)
if 'unblind' in OTHER:
    ASIMOV=""

print("We are using the asimov dataset")
OPTIONS="{OPTIONS} -L ttW_multilepton/functionsTTW.cc --mcc ttW_multilepton/lepchoice-ttW-FO.txt --mcc ttW_multilepton/mcc-METchoice-prefiring.txt {PROMPTSUB} --neg   --threshold 0.01 {ASIMOV} ".format(OPTIONS=OPTIONS,PROMPTSUB=PROMPTSUB,ASIMOV=ASIMOV) # neg necessary for subsequent rebin #
CATPOSTFIX=""
MCASUFFIX="mcdata-frdata"

DOFILE = ""

GENN = ""

if OBSERVABLE == "inclusive":
    FUNCTION_2L="0"
    FUNCTION_3L="0"
    CATBINS    ="[-0.5,0.5]"
    FUNCTION_CR_3L='''"ttH_3l_clasifier(nJet25,nBJetMedium25)" "[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5]" '''
    FUNCTION_CR_4L='''"ttH_4l_clasifier(nJet25,nBJetMedium25,mZ2)" "[0.5,1.5,2.5,3.5,4.5]" '''
    if "gen" in OTHER:       
       GENN = "Gen_"

elif OBSERVABLE == "asymmetry":
    FUNCTION_3L="ttW_charge_asymmetry_v4(hasOSSF,nJet30, abs(positive_lepton_eta)-abs(negative_lepton_eta),nBJetMedium30, mZ_OSSF)"
    CATBINS    ="[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5]"
    CATPOSTFIX=" -E ^met "
else:
    if "gen" in OTHER:
        GENN = "Gen_"
        FUNCTION_2L=all_vars[(OBSERVABLE,REGION)].FUNCTION_2L
        CATBINS=all_vars[(OBSERVABLE,REGION)].CATBINS_Gen

    else:
        FUNCTION_2L=all_vars[(OBSERVABLE,REGION)].FUNCTION_2Lreco
        CATBINS=all_vars[(OBSERVABLE,REGION)].CATBINS

if "gen" in OTHER:
    SYSTS="--unc ttW_multilepton/systsUnc_gen.txt"


if REGION == "2lss":
    OPT_2L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_2lss"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    if "gen" in OTHER:
        OPT_2L = OPT_2L.replace('-W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_2lss"','')
    CATPOSTFIX=""
    CHARGE = ""
    if "charge_flav_split" in OTHER or "chargesplit" in OTHER:
       CHARGE = "chargebiname"
       print(CHARGE)

    TORUN='''python {SCRIPT} {DOFILE} ttW_multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}{OBSERVABLE}.txt ttW_multilepton/2lss_tight.txt "{FUNCTION_2L}" "{CATBINS}" {SYSTS} {OPT_2L} --binname ttW_2lss_0tau_{GEN}{OBS}_{YEAR}{CHARGE} --year {YEAR}  '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, OBSERVABLE="-"+OBSERVABLE, FUNCTION_2L=FUNCTION_2L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_2L=OPT_2L, YEAR=YEAR, GEN=GENN,OBS=OBSERVABLE,CHARGE = CHARGE)
    if "gen" in OTHER:
        MCA = '''ttW_multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}{OBSERVABLE}.txt'''.format(MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, OBSERVABLE="-"+OBSERVABLE)
        TORUN = TORUN.replace(MCA,"ttW_multilepton/mca-includes/mca-2lss-sigprompt-gen.txt")
        TORUN = TORUN.replace("ttW_multilepton/2lss_tight.txt","ttW_multilepton/2lss_fiducial.txt")
    if "chargesplit" in OTHER:
        print( submit.format(command=TORUN.replace("chargebiname","_positive")+ " -E ^plusplus")) #tra-tra
        print( submit.format(command=TORUN.replace("chargebiname","_negative")+ " -E ^minusminus")) #malamente
        os.system(submit.format(command=TORUN.replace("chargebiname","_positive")+ " -E ^plusplus"))
        os.system(submit.format(command=TORUN.replace("chargebiname","_negative")+ " -E ^minusminus"))
    if "charge_flav_split" in OTHER:
        print( submit.format(command=TORUN.replace("chargebiname","_positive_ee")+ " -E ^plusplus -E ^ee")) # ee tra-tra
        print( submit.format(command=TORUN.replace("chargebiname","_positive_em")+ " -E ^plusplus -E ^em")) # emu tra-tra
        print( submit.format(command=TORUN.replace("chargebiname","_positive_mm")+ " -E ^plusplus -E ^mm")) # mumu tra-tra
        
        print( submit.format(command=TORUN.replace("chargebiname","_negative_ee")+ " -E ^minusminus -E ^ee")) #ee malamente
        print( submit.format(command=TORUN.replace("chargebiname","_negative_em")+ " -E ^minusminus -E ^em")) #emu malamente
        print( submit.format(command=TORUN.replace("chargebiname","_negative_mm")+ " -E ^minusminus -E ^mm")) #mumu malamente
        os.system( submit.format(command=TORUN.replace("chargebiname","_positive_ee")+ " -E ^plusplus -E ^ee")) # ee tra-tra
        os.system( submit.format(command=TORUN.replace("chargebiname","_positive_em")+ " -E ^plusplus -E ^em")) # emu tra-tra
        os.system( submit.format(command=TORUN.replace("chargebiname","_positive_mm")+ " -E ^plusplus -E ^mm")) # mumu tra-tra
        
        os.system( submit.format(command=TORUN.replace("chargebiname","_negative_ee")+ " -E ^minusminus -E ^ee")) #ee malamente
        os.system( submit.format(command=TORUN.replace("chargebiname","_negative_em")+ " -E ^minusminus -E ^em")) #emu malamente
        os.system( submit.format(command=TORUN.replace("chargebiname","_negative_mm")+ " -E ^minusminus -E ^mm")) #mumu malamente
        
    else:
        os.system( submit.format(command=TORUN))
        print( submit.format(command=TORUN))

if (REGION == "3l" and "diff" in OTHER):

    OPT_2L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_3l"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    if "gen" in OTHER:
        OPT_2L = OPT_2L.replace('-W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_3l"','')
    CATPOSTFIX=""
    FLAVOR = "allflav"
    TORUN='''python {SCRIPT} {DOFILE} ttW_multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}{OBSERVABLE}.txt ttW_multilepton/3l_tight.txt "{FUNCTION_2L}" "{CATBINS}" {SYSTS} {OPT_2L} --binname ttW_3l_0tau_{GEN}{OBS}_{YEAR}_{FLAV} --year {YEAR} -E nbtagdiff -X ^2b1B '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, OBSERVABLE="-"+OBSERVABLE, FUNCTION_2L=FUNCTION_2L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_2L=OPT_2L, YEAR=YEAR, GEN=GENN,OBS=OBSERVABLE,FLAV=FLAVOR)
    if "gen" in OTHER:
        MCA = '''ttW_multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}{OBSERVABLE}.txt'''.format(MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, OBSERVABLE="-"+OBSERVABLE)
        TORUN = TORUN.replace(MCA,"ttW_multilepton/mca-includes/mca-3l-sigprompt-gen.txt")
        TORUN = TORUN.replace("ttW_multilepton/3l_tight.txt","ttW_multilepton/3l_fiducial.txt")
    if "flav_split" in OTHER:
       #os.system(submit.format(command=TORUN.replace("allflav","eee")+ "-E eee"))
       #os.system(submit.format(command=TORUN.replace("allflav","eem")+ "-E eem"))
       #os.system(submit.format(command=TORUN.replace("allflav","emm")+ "-E emm"))
       #os.system(submit.format(command=TORUN.replace("allflav","mmm")+ "-E mmm"))
       print(submit.format(command=TORUN.replace("allflav","eee")+ "-E eee"))
       print(submit.format(command=TORUN.replace("allflav","eem")+ "-E eem"))
       print(submit.format(command=TORUN.replace("allflav","emm")+ "-E emm"))
       print(submit.format(command=TORUN.replace("allflav","mmm")+ "-E mmm"))

if REGION == "3l" and OBSERVABLE == "asymmetry":
    OPT_3L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_3l"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    TORUN='''python {SCRIPT} {DOFILE} ttW_multilepton/mca-3l-mcdata-frdata-leptoncharge.txt ttW_multilepton/3l_tight.txt "{FUNCTION_3L}" "{CATBINS}" {SYSTS} {OPT_3L} --binname ttW_3l_{OBS}_{YEAR} --year {YEAR}{CATPOSTFIX} '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_3L=FUNCTION_3L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_3L=OPT_3L, YEAR=YEAR, OBS=OBSERVABLE, CATPOSTFIX=CATPOSTFIX)
    print( submit.format(command=TORUN))

if REGION == "3l" and OBSERVABLE == "inclusive":
    OPT_3L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_3l"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    TORUN='''python {SCRIPT} {DOFILE} ttW_multilepton/mca-3l-mcdata-frdata-inclusive.txt  ttW_multilepton/3l_tight.txt "{FUNCTION_3L}" "{CATBINS}" {SYSTS} {OPT_3L} --binname ttW_3l_{OBS}_{YEAR} --year {YEAR}{CATPOSTFIX} '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_3L=FUNCTION_3L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_3L=OPT_3L, YEAR=YEAR, OBS=OBSERVABLE, CATPOSTFIX=CATPOSTFIX)
    print( submit.format(command=TORUN))

if  REGION == "cr_3l" and OBSERVABLE == "inclusive":
    OPT_3L='{T3L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_3l"'.format(T3L=T3L,OPTIONS=OPTIONS)
    CATPOSTFIX="_cr"
    OPT_3L="{OPT_3L} -I ^Zveto -E ^underflowVeto3l -X ^2j -X ^2b1B".format(OPT_3L=OPT_3L)
    CATFUNC="ttH_3l_ifflav(LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId)"
    CATBINS="[0.5,1.5,2.5,3.5,4.5]"
    CATNAMES=",".join( map( lambda x : x+CATPOSTFIX, 'eee,eem,emm,mmm'.split(',')))
    TORUN = '''python {SCRIPT} {DOFILE} ttW_multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}{OBSERVABLE}.txt ttW_multilepton/3l_tight.txt {FUNCTION_CR_3L} {SYSTS} {OPT_3L} --binname ttW_cr_3l_{YEAR} --categorize "{CATFUNC}" "{CATBINS}" {CATNAMES} --year {YEAR}'''.format( SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX,MCAOPTION=MCAOPTION,OBSERVABLE="-"+OBSERVABLE,FUNCTION_CR_3L=FUNCTION_CR_3L,SYSTS=SYSTS,OPT_3L=OPT_3L,YEAR=YEAR,CATFUNC=CATFUNC,CATBINS=CATBINS,CATNAMES=CATNAMES)
    print( submit.format(command=TORUN))
    os.system(submit.format(command=TORUN))

if REGION == "cr_4l" and OBSERVABLE == "inclusive":
    OPT_4L='{T4L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_4l*triggerSF_3l"'.format(T4L=T4L,OPTIONS=OPTIONS)
    OPT_4L="{OPT_4L} -I ^Zveto  -E ^underflowVeto4l -X 2j -X 2b1B".format(OPT_4L=OPT_4L)
    CATPOSTFIX="_cr_4l";
    TORUN = 'python {SCRIPT} {DOFILE} ttW_multilepton/mca-4l-{MCASUFFIX}{MCAOPTION}.txt ttW_multilepton/4l_tight.txt {FUNCTION_CR_4L} {SYSTS} {OPT_4L} --binname ttW{CATPOSTFIX}_{YEAR} --year {YEAR} '.format(SCRIPT=SCRIPT, DOFILE=DOFILE,MCASUFFIX=MCASUFFIX,MCAOPTION=MCAOPTION, FUNCTION_CR_4L=FUNCTION_CR_4L,SYSTS=SYSTS,OPT_4L=OPT_4L,CATPOSTFIX=CATPOSTFIX,YEAR=YEAR)
    print(submit.format(command=TORUN))
    os.system(submit.format(command=TORUN))

