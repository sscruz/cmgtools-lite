# taken from vrbouza's original script

from copy import deepcopy
import os, sys, argparse
from differential_variables import all_vars




basecommand = "sbatch -p batch --wrap 'combineTool.py -M MultiDimFit {algosettings} --setParameters {setpars} --split-points 1 --floatOtherPOIs=1 --saveInactivePOI 1 {parallel} {queue} {extra} --robustFit 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 --setParameterRanges {minmaxlist} --squareDistPoiStep --autoRange 4 -m 125'"

individual_scaff = {
    "btag": [
        "CMS_ttWl_btag_LF_2016APV", 
        "CMS_ttWl_btag_LF", 
        "CMS_ttWl_btag_HF_2016APV", 
        "CMS_ttWl_btag_HF", 
        "CMS_ttWl_btag_LF_2016", 
        "CMS_ttWl_btag_LF_2017", 
        "CMS_ttWl_btag_LF_2018", 
        "CMS_ttWl_btag_HF_2016", 
        "CMS_ttWl_btag_HF_2017", 
        "CMS_ttWl_btag_HF_2018"
    ], 
    "jesjerpileup": [
        "CMS_scale_j_BBEC1_2016", 
        "CMS_scale_j_BBEC1_2018", 
        "CMS_scale_j_BBEC1_2017", 
        "CMS_scale_j_RelativeBal", 
        "CMS_scale_j_FlavorPureGluon", 
        "CMS_scale_j_FlavorPureQuark", 
        "CMS_scale_j_FlavorPureCharm", 
        "CMS_scale_j_FlavorPureBottom", 
        "CMS_scale_j_RelativeSample_2016APV", 
        "CMS_scale_j_BBEC1", 
        "CMS_res_j_barrel_2016APV", 
        "CMS_scale_j_Absolute", 
        "CMS_scale_j_BBEC1_2016APV", 
        "CMS_scale_j_Absolute_2016APV", 
        "CMS_ttWl_pileup", 
        "CMS_scale_j_Absolute_2018", 
        "CMS_scale_j_Absolute_2016", 
        "CMS_scale_j_Absolute_2017", 
        "CMS_scale_j_RelativeSample_2018", 
        "CMS_jesHEMIssue", 
        "CMS_ttWl_UnclusteredEn", 
        "CMS_scale_j_RelativeSample_2017", 
        "CMS_scale_j_RelativeSample_2016", 
        "CMS_res_j_endcap1_2018", 
        "CMS_res_j_endcap1_2016", 
        "CMS_res_j_endcap1_2017", 
        "CMS_res_j_endcap1_2016APV", 
        "CMS_res_j_barrel_2018", 
        "CMS_res_j_barrel_2017", 
        "CMS_res_j_barrel_2016"
    ], 
    "lumi": [
        "lumi_13TeV_1718", 
        "lumi_13TeV_2016APV", 
        "lumi_13TeV_correlated", 
        "lumi_13TeV_2018", 
        "lumi_13TeV_2016", 
        "lumi_13TeV_2017"
    ], 
    "Norm_ttz_wz_zz": [
        "CMS_ttWl_TTZ_lnU", 
        "CMS_ttWl_WZ_lnU", 
        "CMS_ttWl_ZZ_lnU", 
    ], 
    "modeling_norm": [
        "QCDscale_ttZ", 
        "QCDscale_ttH", 
        "CMS_ttWl_Rares",
        "CMS_ttWl_tZq", 
        "CMS_ttWl_ttVV",  
        "CMS_ttWl_Convs", 
        "CMS_ttWl_QF",
        "CMS_ttWl_VVV",  
        "QCDscale_tHW", 
        "QCDscale_tHq",
        "rgx{BR_.*}"
    ], 
    "modeling_shape": [
        "CMS_ttWl_EWK_btag", 
        "rgx{CMS_ttWl_thu_shape_ttH.*}", 
        "rgx{CMS_ttWl_thu_shape_ttZ.*}", 
        "pdf_gg", 
        "rgx{CMS_ttWl_thu_shape_ZZ.*}", 
        "rgx{CMS_ttWl_thu_shape_ttW.*}", 
        "pdf_qg", 
        "rgx{CMS_ttWl_thu_shape_tHq.*}", 
        "rgx{CMS_ttWl_thu_shape_tHW.*}", 
        "pdf_Higgs_ttH", 
        "pdf_TTWW", 
        "rgx{CMS_ttWl_thu_shape_WZ.*}", 
        "pdf_qqbar", 
        "CMS_ttWl_EWK_jet",
        "rgx{QCDpdf_ACCEPT.*}",
        "alphaS",
        "FSR",
        "ISR_ttW",
        "ISR_ttH",
        "ISR_ttZ",
        "ISR_tZq",
        "rgx{CMS_ttWl_thu_shape_tZq.*}",
        "rgx{CMS_ttWl_thu_shape_VVV.*}",
        "rgx{CMS_ttWl_thu_shape_ttVV.*}",
        "rgx{CMS_ttWl_thu_shape_Rares.*}",

    ], 
    "nonprompt": [
        "CMS_ttWl_FRm_pt", 
        "CMS_ttWl_FRe_be", 
        "CMS_ttWl_FRe_pt", 
        "CMS_ttWl_FRm_norm", 
        "CMS_ttWl_FRe_norm", 
        "CMS_ttWl_FRm_be"
    ], 
    "trigger_leptons": [
        "CMS_eff_ttWl_e", 
        "CMS_eff_ttWl_m", 
        "CMS_ttWl18_trigger_ee", 
        "CMS_ttWl16APV_trigger_ee", 
        "CMS_ttWl18_trigger_mm", 
        "CMS_ttWl16APV_trigger_em", 
        "CMS_ttWl16APV_trigger_mm", 
        "CMS_ttWl16_trigger_ee", 
        "CMS_ttWl16_trigger_em", 
        "CMS_ttWl16_trigger_mm", 
        "CMS_ttWl18_trigger_em", 
        "CMS_ttWl17_trigger_mm", 
        "CMS_ttWl17_trigger_ee", 
        "CMS_ttWl17_trigger_em", 
        "CMS_ttWl17_L1PreFiring", 
        "CMS_ttWl16_L1PreFiring"
    ],
    'mc_stat': ["rgx{prop_.*}"],
}

individual_list = [ what for what in individual_scaff]


def calculateRelativeUncertainties(task):
    inpath, varName, ncores, pretend, verbose, extra, doobs, doblind = task

    redo=True
    bins_detector = eval(all_vars[(varName,'2lss')].CATBINS)
    ndetectorbins   = len(bins_detector) - 1
    bins_particle = eval(all_vars[(varName,'2lss')].CATBINS_Gen)
    nparticlebins   = len(bins_particle) - 1

    npoints = 20
    
    for iP in ["", "/individual", "/nominal"]:
        os.system("mkdir -p " + inpath + iP)

    doBatch = False

    #print userstdirrw
    POIs    = ["r_TTW_%s_bin%d"%(varName,i) for i in range(nparticlebins)]
    indGroup = deepcopy(individual_scaff)

    thecard = "../ws_"+varName+'_2lss.root'


    ##################### OLD
    # First, we calculate the nominal files that we need.
    for poi in POIs:
      cumulative = [x for x in POIs if x != poi]

      # nominal_POI
      if donominal_1 or donominal_2:
        if not os.path.isfile(inpath + "/nominal/higgsCombinenominal_{p}.MultiDimFit.mH125.root".format(p = poi)) or redo:
            nomcomm    = basecommand.format(algosettings = "--algo grid --points " + str(npoints),
                                            setpars      = ",".join([el + "=1" for el in POIs]),
                                            queue        = "" if not doBatch else "--job-mode slurm --task-name nominal_" + poi,
                                            parallel     = "" if not ncores  else "--parallel " + str(ncores),
                                            extra        = '-n nominal_{p} {card} -P {p}'.format(p = poi, card = thecard),
                                            #extra        = '-n nominal_{p} {card} -P {p} --freezeParameters {c}'.format(p = poi, card = thecard, c = ",".join(cumulative))
                                            minmaxlist   = ":".join([el + "=0,3" for el in POIs]),
                            )
            if donominal_1:    
               if not pretend: os.system("cd {path}; rm ./higgsCombinenominal_{p}.POINTS*; cd -".format(path = inpath + "/nominal", p = poi))

               print "\nCommand:", "cd {p}; {cmd}; cd -".format(p = inpath + "/nominal", cmd = nomcomm)
               if not pretend: os.system("cd {p}; {cmd}; cd -".format(p = inpath + "/nominal", cmd = nomcomm))
            if donominal_2:
               nomcomm  = 'hadd -f higgsCombinenominal_{p}.MultiDimFit.mH125.root higgsCombinenominal_{p}.POINTS.*.MultiDimFit.mH125.root'.format(p = poi)
               print "\nCommand:", "cd {p}; {cmd}; cd -".format(p = inpath + "/nominal", cmd = nomcomm) 
               if not pretend: os.system("cd {p}; {cmd}; cd -".format(p = inpath + "/nominal", cmd = nomcomm))

        # bestfit_POI
      elif doBF:
        if not os.path.isfile(inpath + "/nominal/higgsCombinebestfit_{p}.MultiDimFit.mH125.root".format(p = poi)) or redo:

            if not pretend and os.path.isfile(inpath + "/nominal/higgsCombinebestfit_{p}.MultiDimFit.mH125.root".format(p = poi)):
                os.system("cd {path}; rm ./higgsCombinebestfit_{p}.MultiDimFit.mH125.root; cd -".format(path = inpath + "/nominal", p = poi))
            gridcomm = basecommand.format(algosettings = "--algo none",
                                            setpars    = ",".join([el + "=1" for el in POIs]),
                                            queue      = "",
                                            parallel   = "",
                                            extra      = '-n bestfit_{p} --saveWorkspace {card} -P {p}'.format(p = poi, card = thecard),
                                            minmaxlist   = ":".join([el + "=0,3" for el in POIs])
                                         )
            print "\nCommand:", "cd {p}; {cmd}; cd -".format(p = inpath + "/nominal", cmd = gridcomm)
            if not pretend: os.system("cd {p}; {cmd}; cd -".format(p = inpath + "/nominal", cmd = gridcomm))

    if not (donominal_1) and not (donominal_2) and not(doBF) and splitting:
     for poi in POIs:
        #cumulative = [x for x in POIs if x != poi]
        cumulative = []
        fileList   = []

        for gr in individual_list:
            cumulative += indGroup[gr]
            fileList.append("'higgsCombine{gp}.MultiDimFit.mH125.root:Freeze += {g}:{i}'".format(gp = gr + '_' + poi,
                                                                                                 g  = gr,
                                                                                                 i  = individual_list.index(gr)))

            if not os.path.isfile(inpath + "/individual/higgsCombine{g}_{p}.MultiDimFit.mH125.root".format(g = gr, p = poi)) or redo:
                thecomm = basecommand.format(algosettings = "--algo grid --points " + str(npoints),
                                            setpars      = ",".join([el + "=1" for el in POIs]),
                                            queue        = "" if not doBatch else "--job-mode slurm --task-name " + gr + "_" + poi,
                                            parallel     = "" if not ncores  else "--parallel " + str(ncores),
                                            #extra        = '-P {p} -n {g}_{p} ../nominal/higgsCombinebestfit_{p}.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeParameters {c}'.format(p = poi, g = gr, c = ",".join(cumulative)),
                                            extra        = '-P {p} -n {g}_{p} ../nominal/higgsCombinebestfit_{p}.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeParameters {c} --saveFitResult --out {op}'.format(p = poi, g = gr, c = ",".join(cumulative), op = inpath + "/individual"),
                                            minmaxlist   = ":".join([el + "=0,3" for el in POIs]),
                )

                #if not pretend: os.system("cd {path}; rm ./higgsCombine{g}_{p}.POINTS*; cd -".format(path = inpath + "/individual", p = poi, g = gr))
                #print "\nCommand:", "cd {p}; {cmd}; cd -".format(p = inpath + "/individual", cmd = thecomm)
                #if not pretend: os.system("cd {p}; {cmd}; cd -".format(p = inpath + "/individual", cmd = thecomm))

                tmpcomm = 'hadd -f higgsCombine{gp}.MultiDimFit.mH125.root higgsCombine{gp}.POINTS.*.MultiDimFit.mH125.root'.format(gp = gr + '_' + poi)


                print "\nCommand:", "cd {p}; {cmd}; cd -".format(p = inpath + "/individual", cmd = tmpcomm)
                if not pretend: os.system("cd {p}; {cmd}; cd -".format(p = inpath + "/individual", cmd = tmpcomm))


        if not os.path.isfile(inpath + "/individual/outputfit_{p}.txt".format(p = poi)) or redo:
            thecomm = "python /nfs/fanae/user/clara/ttW_diff_new/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/ttW_multilepton/plot1DScan.py ../nominal/higgsCombinenominal_{p}.MultiDimFit.mH125.root --others {l1} --breakdown {l2},stat --POI {p} ".format( # need a better way of doing this... unfortunately CMSSW_BASE is in the combine set-up (10_2) 
                p  = poi,
                l1 = ' '.join(fileList),
                l2 = ','.join(individual_list))
            print "\nCommand:", "cd {p}; {cmd}; cd -".format(p = inpath + "/individual", cmd = thecomm)
            if not pretend: os.system("cd {p}; {cmd}; cd -".format(p = inpath + "/individual", cmd = thecomm))

            thecomm2 = 'mv scan.pdf scan_{p}.pdf; mv scan.png scan_{p}.png; mv scan.root scan_{p}.root; mv outputfit.txt outputfit_{p}.txt'.format(p = poi)
            print "\nCommand:", "cd {p}; {cmd}; cd -".format(p = inpath + "/individual", cmd = thecomm2)
            if not pretend: os.system("cd {p}; {cmd}; cd -".format(p = inpath + "/individual", cmd = thecomm2))
    

    return




if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage = "python nanoAOD_checker.py [options]", description = "Checker tool for the outputs of nanoAOD production (NOT postprocessing)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inpath',     '-i', metavar = 'inpath',     dest = "inpath",   required = False, default = "./temp/differential/")
    parser.add_argument('--variable',   '-v', metavar = 'variable',   dest = "variable", required = False, default = "all")
    parser.add_argument('--extraArgs',  '-e', metavar = 'extra',      dest = "extra",    required = False, default = "")
    parser.add_argument('--nthreads',   '-j', metavar = 'nthreads',   dest = "nthreads", required = False, default = 0, type = int)
    parser.add_argument('--pretend',    '-p', action  = "store_true", dest = "pretend",  required = False, default = False)
    parser.add_argument('--verbose',    '-V', action  = "store_true", dest = "verbose",  required = False, default = False)
    parser.add_argument('--doObserved', '-O', action  = "store_true", dest = "doobs",    required = False, default = False)
    parser.add_argument('--blindSignalStrength','-b',action="store_true",dest="blindmu", required = False, default = False)
    parser.add_argument('--donominal_1','-N1',action="store_true",dest="donominal_1", required = False, default = False)
    parser.add_argument('--donominal_2','-N2',action="store_true",dest="donominal_2", required = False, default = False)
    parser.add_argument('--doBF','-B',action="store_true",dest="doBF", required = False, default = False)
    parser.add_argument('--splitting','-S',action="store_true",dest="splitting", required = False, default = False)

    args     = parser.parse_args()
    nthreads = args.nthreads
    pretend  = args.pretend
    inpath   = args.inpath
    varName  = args.variable
    verbose  = args.verbose
    extra    = args.extra
    doobs    = args.doobs
    doblind  = args.blindmu
    ncores   = args.nthreads
    donominal_1= args.donominal_1
    donominal_2 = args.donominal_2
    doBF = args.doBF
    splitting = args.splitting
    task=inpath, varName, ncores, pretend, verbose, extra, doobs, doblind

    calculateRelativeUncertainties(task)
