import os, sys
nCores=32
submit = '''sbatch -c %d -p batch  --wrap '{command}' '''%nCores
#submit = '{command}' 


if 'psi' in os.environ['HOSTNAME']:       ORIGIN="/pnfs/psi.ch/cms/trivcat/store/user/sesanche/"; 
elif 'fanae' in os.environ['HOSTNAME']:
    ORIGIN     = "/beegfs/data/nanoAODv9/ttH_differential/"
elif 'gae' in os.environ['HOSTNAME']: 
    ORIGIN    = "/beegfs/data/nanoAODv9/ttH_differential/"


else: 
    raise RuntimeError("You need ntuples to run the analysis :)")

if len(sys.argv) < 4: 
    print 'Sytaxis is %s [outputdir] [year] [region] [observable] [other]'%sys.argv[0]
    raise RuntimeError 
OUTNAME=sys.argv[1]
YEAR=sys.argv[2]
REGION=sys.argv[3]
OBSERVABLE=sys.argv[4]
OTHER=sys.argv[5:] if len(sys.argv) > 5 else ''

if   YEAR == '2016'   : LUMI="16.8"
elif   YEAR == '2016APV': LUMI="19.5"
elif YEAR in '2017': LUMI="41.4"
elif YEAR in '2018': LUMI="59.7"
else:
    raise RuntimeError("Wrong year %s"%YEAR)


#print "Normalizing to {LUMI}/fb".format(LUMI=LUMI);
OPTIONS=" --tree NanoAOD --s2v -j {J} -l {LUMI} -f --WA prescaleFromSkim --split-factor=-1 ".format(LUMI=LUMI,J=nCores)
os.system("test -d cards/{OUTNAME} || mkdir -p cards/{OUTNAME}".format(OUTNAME=OUTNAME))
OPTIONS="{OPTIONS} --od cards/{OUTNAME} ".format(OPTIONS=OPTIONS, OUTNAME=OUTNAME)
if "gen" in OTHER:
   OPTIONS = OPTIONS.replace("--WA prescaleFromSkim","")
   ltext = "-l {LUMI}".format(LUMI=LUMI)


<<<<<<< HEAD
T2L="-P {ORIGIN}/NanoTrees_UL_v2_060422_skim2lss_newfts/{YEAR} --FMCs {{P}}/0_jmeUnc_v1  --FMCs {{P}}/2_btagSF_fixedWP/ --FMCs {{P}}/2_scalefactors_lep/ --Fs {{P}}/4_evtVars --FMCs {{P}}/6_ttWforlepton --FMCs {{P}}/7_Vars_forttWDiff --Fs {{P}}/1_recl   --xf GGHZZ4L_new,qqHZZ4L,tWll,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,TGJets_lep,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,ZGTo2LG,GluGluToHHTo4V,TTTW ".format(ORIGIN=ORIGIN, YEAR=YEAR)
=======
T2L="-P {ORIGIN}/NanoTrees_UL_v2_060422_skim2lss_newfts/{YEAR} --FMCs {{P}}/0_jmeUnc_v1  --FMCs {{P}}/2_btagSF/ --FMCs {{P}}/2_scalefactors_lep/ --Fs {{P}}/4_evtVars --FMCs {{P}}/6_ttWforlepton --Fs {{P}}/7_Vars_forttWDiff --Fs {{P}}/1_recl   --xf GGHZZ4L_new,qqHZZ4L,tWll,WW_DPS,WpWpJJ,WWW_ll,T_sch_lep,GluGluToHHTo2V2Tau,TGJets_lep,WWTo2L2Nu_DPS,GluGluToHHTo4Tau,ZGTo2LG,GluGluToHHTo4V,TTTW ".format(ORIGIN=ORIGIN, YEAR=YEAR)
>>>>>>> 4aeb15c591f7c2ec226d6ba2203a4745856ed5c2

if "gen" in OTHER:
   T2L= "-P {ORIGIN}/NanoTrees_UL_v2_gennoskim/{YEAR} ".format(ORIGIN=ORIGIN, YEAR=YEAR)


T3L=T2L
T4L=T2L

SYSTS="--unc ttW-multilepton/systsUnc.txt --amc --xu CMS_ttWl_WZ_lnU,CMS_ttWl_ZZ_lnU,QCDscale_ttW"
MCAOPTION=""
MCAOPTION=""
ASIMOV="--asimov signal"
SCRIPT= "makeShapeCardsNew.py"
PROMPTSUB="--plotgroup data_fakes+=.*_promptsub"

if 'unblind' in OTHER:
    ASIMOV=""

print "We are using the asimov dataset"
OPTIONS="{OPTIONS} -L ttH-multilepton/functionsTTH.cc --mcc ttW-multilepton/lepchoice-ttW-FO.txt --mcc ttW-multilepton/mcc-METchoice-prefiring.txt {PROMPTSUB} --neg   --threshold 0.01 {ASIMOV} ".format(OPTIONS=OPTIONS,PROMPTSUB=PROMPTSUB,ASIMOV=ASIMOV) # neg necessary for subsequent rebin #
CATPOSTFIX=""
MCASUFFIX="mcdata-frdata"

DOFILE = ""

<<<<<<< HEAD
availableObservables = ['inclusive', 'njets','nbjets','lep1_pt','lep1_eta',"dR_ll","max_eta",'jet1_pt','deta_llss',"HT",'dR_lbloose', 'dR_lbmedium',"asymmetry_withbees","mindr_lep1_jet30","asymmetry_smart_nocharge","asymmetry_v4"]
=======
availableObservables = ['inclusive', 'njets','nbjets','lep1_pt','lep1_eta',"dR_ll","max_eta",'jet1_pt','deta_llss',"HT",'dR_lbloose', 'dR_lbmedium',"mindr_lep1_jet25", "asymmetry"]
>>>>>>> 4aeb15c591f7c2ec226d6ba2203a4745856ed5c2

if OBSERVABLE == "inclusive":
    FUNCTION_2L="0"
    CATBINS    ="[-0.5,0.5]"
    

elif OBSERVABLE == "njets":
    FUNCTION_2L="nJet25"
    if "gen" in OTHER:
        FUNCTION_2L="nDressSelJet"
        SYSTS = ""
    CATBINS    ="[2.5,3.5,4.5,5.5,6.5,7.5]"

elif OBSERVABLE == "nbjets":
    FUNCTION_2L="nBJetLoose25"
    if "gen" in OTHER:
        FUNCTION_2L="nDressBSelJet"
        SYSTS = ""
    CATBINS    ="[0.5,1.5,2.5,3.5]"

elif OBSERVABLE == "lep1_pt":
    FUNCTION_2L="LepGood1_conePt"
    CATBINS    = "[25,40,50,75,100,125,150,187,225,350,500]"
    if "gen" in OTHER:
        FUNCTION_2L="GenDressedLepton_pt[iDressSelLep[0]]"
        CATBINS    ="[25,50,100,150,225,500]"
        SYSTS = ""

elif OBSERVABLE == "dR_ll":
    FUNCTION_2L="deltaR(LepGood1_eta,LepGood1_phi,LepGood2_eta,LepGood2_phi)"
    CATBINS    = "[0.75,1.5,2.0,2.5,3.0,3.5,4.5,5]"
    if "gen" in OTHER:
        FUNCTION_2L="deltaR(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_phi[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]],GenDressedLepton_phi[iDressSelLep[1]])"
        CATBINS    ="[0.0,1.5,2.5,3.5,5]"
        SYSTS = ""

elif OBSERVABLE == "lep1_eta":
    FUNCTION_2L="abs(LepGood1_eta)"
    CATBINS    = "[0.,0.45,0.9,1.1,1.2,1.85,2.5]"
    if "gen" in OTHER:
        FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]])"
        CATBINS    ="[0.,0.9,1.2,2.5]"
        SYSTS = ""

elif OBSERVABLE == "max_eta":
    FUNCTION_2L="max(LepGood1_eta,LepGood2_eta)"
    CATBINS    = "[0.0,0.45,0.75,1.25,1.5,1.75,2.0,2.25,2.5]"
    if "gen" in OTHER:
        FUNCTION_2L="max(GenDressedLepton_eta[iDressSelLep[0]],GenDressedLepton_eta[iDressSelLep[1]])"
        CATBINS    ="[0.0,0.75,1.5,2.0,2.5]"
        SYSTS = ""


elif OBSERVABLE == "jet1_pt":
    FUNCTION_2L="JetSel_Recl_pt[0]"
    CATBINS    ="[25,40,50,75,100,125,150,187,225,350,500]"
    if "gen" in OTHER:
        FUNCTION_2L="GenJet_pt[iDressSelJet[0]]"
        CATBINS    ="[25,50,100,150,225,500]"
        SYSTS = ""

elif OBSERVABLE == "deta_llss":
    FUNCTION_2L="abs(LepGood1_eta-LepGood2_eta)"
    CATBINS    ="[0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4]"
    if "gen" in OTHER:
        FUNCTION_2L="abs(GenDressedLepton_eta[iDressSelLep[0]]-GenDressedLepton_eta[iDressSelLep[1]])"
        CATBINS    ="[0.0,0.4,0.8,1.2,1.6,2.0,2.4]"
        SYSTS = ""

<<<<<<< HEAD
=======
<<<<<<< HEAD
elif OBSERVABLE == "asymmetry":
=======
>>>>>>> 4aeb15c591f7c2ec226d6ba2203a4745856ed5c2
elif OBSERVABLE == "dR_lbmedium":
    FUNCTION_2L="dR_lbmedium"
    CATBINS    ="[0, 0.5, 1.0,1.25, 1.5,1.75, 2.0, 2.5, 3.0]"
    if "gen" in OTHER:
        FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
        SYSTS = ""

elif OBSERVABLE == "dR_lbloose":
    FUNCTION_2L="dR_lbloose"
    CATBINS    ="[0, 0.5, 1.0,1.25, 1.5,1.75, 2.0, 2.5, 3.0]"
    if "gen" in OTHER:
        FUNCTION_2L="dR_DressBSelJet_DressSelLep1"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
        SYSTS = ""

<<<<<<< HEAD
elif OBSERVABLE == "mindr_lep1_jet30":
    FUNCTION_2L="mindr_lep1_jet30"
=======
elif OBSERVABLE == "mindr_lep1_jet25":
    FUNCTION_2L="mindr_lep1_jet25"
>>>>>>> 4aeb15c591f7c2ec226d6ba2203a4745856ed5c2
    CATBINS    ="[0, 0.5, 1.0,1.25, 1.5,1.75, 2.0, 2.5, 3.0]"
    if "gen" in OTHER:
        FUNCTION_2L="mindr_DressSelLep1_DressSelJet"
        CATBINS    ="[0, 1.0, 1.5, 2.0, 3.0]"
        SYSTS = ""

elif OBSERVABLE == "HT":
<<<<<<< HEAD
    FUNCTION_2L="htJet30j_Recl"
=======
    FUNCTION_2L="htJet25j_Recl"
>>>>>>> 4aeb15c591f7c2ec226d6ba2203a4745856ed5c2
    CATBINS    ="[0.0,100,200.,300.,400.,500.,600.,800.,1000.]"
    if "gen" in OTHER:
        FUNCTION_2L="Gen_HT"
        CATBINS    ="[0.0,200.,400.,600.,1000.]"
        SYSTS = ""

elif OBSERVABLE == "asymmetry_withbees":
    FUNCTION_3L="ttW_charge_asymmetry_simple_withbees(hasOSSF,nJet30, LepGood1_charge+LepGood2_charge+LepGood3_charge, abs(positive_lepton_eta)-abs(negative_lepton_eta),nBJetMedium30)"
    CATBINS    ="[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5,32.5,33.5,34.5,35.5,36.5,37.5,38.5,39.5]"
    CATPOSTFIX=" -E ^met "
elif OBSERVABLE == "asymmetry_smart_nocharge":
    FUNCTION_3L="ttW_charge_asymmetry_simple_withbees_nocharge(hasOSSF,nJet30, abs(positive_lepton_eta)-abs(negative_lepton_eta),nBJetMedium30)"
    CATBINS    ="[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5]"
    CATPOSTFIX=" -E ^met "
elif OBSERVABLE == "asymmetry_v4":
>>>>>>> 1f572b998daf1849eab263bab13ef48e8d3311bf
    FUNCTION_3L="ttW_charge_asymmetry_v4(hasOSSF,nJet30, abs(positive_lepton_eta)-abs(negative_lepton_eta),nBJetMedium30, mZ_OSSF)"
    CATBINS    ="[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5]"
    CATPOSTFIX=" -E ^met "

if "gen" in OTHER:
   signals_remove = []

else:
   signals_remove = [ 'TTW_%s.*'%s for s in availableObservables if s!= OBSERVABLE]     
GENN = ""
if "gen" in OTHER:
   GENN = "Gen_"

if REGION == "2lss":
    OPT_2L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year, suberaId)"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    if "gen" in OTHER:
        OPT_2L = OPT_2L.replace('-W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year, suberaId)"','')
    CATPOSTFIX=""

    TORUN='''python {SCRIPT} {DOFILE} ttW-multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}.txt ttW-multilepton/2lss_tight.txt "{FUNCTION_2L}" "{CATBINS}" {SYSTS} {OPT_2L} --binname ttW_2lss_0tau_{GEN}{OBS}_{YEAR} --year {YEAR} --xp {signals_remove} '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_2L=FUNCTION_2L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_2L=OPT_2L, signals_remove=','.join(signals_remove), YEAR=YEAR, GEN=GENN,OBS=OBSERVABLE)
    if "gen" in OTHER:
        TORUN = TORUN.replace("--xp","")
        TORUN = TORUN.replace("ttW-multilepton/mca-2lss-mcdata-frdata.txt","ttW-multilepton/mca-includes/mca-2lss-sigprompt-gen.txt")
        TORUN = TORUN.replace("ttW-multilepton/2lss_tight.txt","ttW-multilepton/2lss_fiducial.txt")
    #os.system( submit.format(command=TORUN))
    print( submit.format(command=TORUN))


if REGION == "3l":
    OPT_3L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_3l*triggerSF_3l"'.format(T2L=T2L, OPTIONS=OPTIONS, YEAR=YEAR)
    TORUN='''python {SCRIPT} {DOFILE} ttW-multilepton/mca-3l-mcdata-frdata-leptoncharge.txt ttW-multilepton/3l_tight.txt "{FUNCTION_3L}" "{CATBINS}" {SYSTS} {OPT_3L} --binname ttW_3l_{OBS}_{YEAR} --year {YEAR} --xp {signals_remove} {CATPOSTFIX} '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_3L=FUNCTION_3L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_3L=OPT_3L, signals_remove=','.join(signals_remove), YEAR=YEAR, OBS=OBSERVABLE, CATPOSTFIX=CATPOSTFIX)
    print submit.format(command=TORUN)
