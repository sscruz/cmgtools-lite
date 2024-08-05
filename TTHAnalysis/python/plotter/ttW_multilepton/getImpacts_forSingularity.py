# get impacts, modified from @vrbouza's script 

import ROOT  as r
import os, sys, argparse, math, json
import warnings as wr
from array import array
from copy  import deepcopy
from multiprocessing import Pool
import CombineHarvester.CombineTools.plotting as plot
import CombineHarvester.CombineTools.combine.rounding as rounding

JOB_PREFIX = """#!/bin/sh
ulimit -s unlimited
set -e
cd %(CMSSW_BASE)s/src
export SCRAM_ARCH=%(SCRAM_ARCH)s
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
eval `scramv1 runtime -sh`
cd %(PWD)s
""" % ({
    'CMSSW_BASE': os.environ['CMSSW_BASE'],
    'SCRAM_ARCH': os.environ['SCRAM_ARCH'],
    'PWD': os.environ['PWD']
})

sys.path.append('{cmsswpath}/src/CMGTools/TTHAnalysis/python/plotter/tw-run2/differential/'.format(cmsswpath = os.environ['CMSSW_BASE']))
from differential_variables import all_vars

r.PyConfig.IgnoreCommandLineOptions = True
r.TH1.AddDirectory(0)

#comm1 = "combineTool.py -M Impacts -d {incard} --doInitialFit --robustFit 1 {ncores} {asimov} {extra} -m 1 -n {prefix} --out {outdir} --redefineSignalPOIs {pois} --floatOtherPOIs 1 --robustHesse 1 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000"
#comm2 = "combineTool.py -M Impacts -d {incard} --robustFit 1 --doFits {ncores} {asimov} {extra} -m 1 -n {prefix} --redefineSignalPOIs {pois} --robustHesse 1 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000"
#comm3 = "combineTool.py -M Impacts -d {incard} -o impacts{prefix}.json {ncores} {asimov} {extra} -m 1 -n {prefix} --redefineSignalPOIs {pois} --robustHesse 1 --robustFit 1 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000"

comm1 = "combineTool.py -M Impacts -d {incard} --doInitialFit --robustFit 1 {ncores} {asimov} {extra} -m 125 -n {prefix} --out {outdir} --redefineSignalPOIs {pois} --floatOtherPOIs 1 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 --cminDefaultMinimizerStrategy 0 --robustHesse 1"
comm2 = "combineTool.py -M Impacts -d {incard} --robustFit 1 --doFits {ncores} {asimov} {extra} -m 125 -n {prefix} --redefineSignalPOIs {pois} --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 --cminDefaultMinimizerStrategy 0 --robustHesse 1 --job-mode slurm_withsingularity  --job-dir ./Logs_impacts   --sub-opts '-p batch'"
comm3 = "combineTool.py -M Impacts -d {incard} -o impacts{prefix}.json {ncores} {asimov} {extra} -m 125 -n {prefix} --redefineSignalPOIs {pois} --robustFit 1  --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 --cminDefaultMinimizerStrategy 0 --robustHesse 1"

nuisanceColours = {
    'Gaussian'          : 1,
    'Poisson'           : 8,
    'p': 9,
    'Unconstrained'     : 39,
    'Unrecognised'      : 2
}

lo_colour = {
    'default': 38,
    'hesse'  : r.kOrange - 3,
    'robust' : r.kGreen + 1
}
hi_colour = {
    'default': 46,
    'hesse'  : r.kBlue,
    'robust' : r.kAzure - 5
}

def GetRounded(nom, e_hi, e_lo):
    if e_hi < 0.0:
        e_hi = 0.0
    if e_lo < 0.0:
        e_lo = 0.0
    rounded = rounding.PDGRoundAsym(nom, e_hi if e_hi != 0.0 else 1.0, e_lo if e_lo != 0.0 else 1.0)
    s_nom = rounding.downgradePrec(rounded[0],rounded[2])
    s_hi = rounding.downgradePrec(rounded[1][0][0],rounded[2]) if e_hi != 0.0 else '0'
    s_lo = rounding.downgradePrec(rounded[1][0][1],rounded[2]) if e_lo != 0.0 else '0'
    return (s_nom, s_hi, s_lo)


def plotImpacts(inputjson, outputname, outputpath, npois, doBlind, varName, regName):
    left_margin   = 0.2
    pullsprop     = 0.37
    label_size    = 0.021
    doEraseStatNuis = False
    canv_width    = 700
    #canv_width    = 900
    canv_height   = 600
    per_page      = 30
    max_pages     = None
    cms_label     = "Internal"
    colour_groups = None
    units         = None
    mainPOI       = None
    xaxistitleoffset = 1
    xaxistitlesize = 0.0265

    externalPullDef = False

    # Dictionary to translate parameter names
    #vl.SysNameTranslator

    # Load the json output of combineTool.py -M Impacts
    data = {}
    with open(inputjson) as jsonfile:
        data = json.load(jsonfile)

    # Set the global plotting style
    plot.ModTDRStyle(l      = left_margin, 
                     b      = 0.10, 
                     width  = canv_width, 
                     height = canv_height)

    # We will assume the first POI is the one to plot
    POIs = [ele['name'] for ele in data['POIs']]
    #POI  = POIs[0]
    #if mainPOI:
        #POI = mainPOI

    poiDict = {}
    for ele in data['POIs']:
        poiDict[ele['name'].encode("utf-8").decode("utf-8")] = ele
    
    #for el in data["params"]:
        #if el["name"] == "dy_norm": print el
    #sys.exit()

    def mean(lst):
        return sum(lst)/len(lst)

    # Sort parameters by the average of the absolute impact on all POIs
    data['params'].sort(key = lambda x: mean([abs(x['impact_' + iP]) for iP in POIs]), reverse = True)
    
    # Delete stat. nuis.?
    if doEraseStatNuis:
        for p in data['params']: 
            print p
            if p['name'].startswith('prop_binch'): 
                print 'deleting', p
                data['params'].remove(p)
    
    # Set the number of parameters per page (show) and the number of pages (n)
    show = per_page
    n    = int(math.ceil(float(len(data['params'])) / float(show)))
    if max_pages is not None and max_pages > 0:
        n = max_pages

    colour_hists       = {}
    colour_group_hists = {}

    if colour_groups is not None:
        colour_groups = {
            x.split('=')[0]: int(x.split('=')[1]) for x in colour_groups.split(',')
        }

    seen_types = set()

    for name, col in nuisanceColours.iteritems():
        colour_hists[name] = r.TH1F()
        plot.Set(colour_hists[name], FillColor = col, Title = name)

    if colour_groups is not None:
        for name, col in colour_groups.iteritems():
            colour_group_hists[name] = r.TH1F()
            plot.Set(colour_group_hists[name], FillColor = col, Title = name)

    for page in xrange(n):
        canv     = r.TCanvas(outputname, outputname)
        n_params = len(data['params'][show * page:show * (page + 1)])
        pdata    = data['params'][show * page:show * (page + 1)]
        print '\t- Doing page %i, have %i parameters' % (page, n_params)

        boxes = []
        for i in xrange(n_params):
            y1 = r.gStyle.GetPadBottomMargin()
            y2 = 1. - r.gStyle.GetPadTopMargin()
            h  = (y2 - y1) / float(n_params)
            y1 = y1 + float(i) * h
            y2 = y1 + h
            box = r.TPaveText(0, y1, 1, y2, 'NDC')
            plot.Set(box, TextSize=0.02, BorderSize=0, FillColor=0, TextAlign=12, Margin=0.005)
            if i % 2 == 0:
                box.SetFillColor(18)
#            if (n_params - i + page * show - 3) <= 0:
            if (n_params - i + page * show) <= 0:
                box.AddText('-')
            else:
#                box.AddText('%i' % (n_params - i + page * show-3))
                box.AddText('%i' % (n_params - i + page * show))
            box.Draw()
            boxes.append(box)

        # Crate and style the pads
        pads = plot.MultiRatioSplitColumns([pullsprop] + [(1. - pullsprop - 0.01)/npois] * npois, [0.] * (npois + 1), [0.] * (npois + 1))
        #pads = plot.MultiRatioSplitColumns([(1. - pullsprop - 0.01)/npois] * npois * 2, [0.] * npois * 2, [0.] * npois * 2)
        for iP in range(npois):
            pads[iP + 1].SetGrid(1, 0)
        pads[0].SetGrid(1, 0)
        pads[0].SetTickx(1)
        pads[1].SetTickx(1)

        h_pulls = r.TH2F("pulls", "pulls", 6, -2.9, 2.9, n_params, 0, n_params)
        g_pulls = r.TGraphAsymmErrors(n_params)
        g_impacts_hi_list = []; g_impacts_lo_list = []
        max_impact_list = [0.] * npois
        for iP in range(npois):
            g_impacts_hi_list.append(r.TGraphAsymmErrors(n_params))
            g_impacts_lo_list.append(r.TGraphAsymmErrors(n_params))
            
        g_check = r.TGraphAsymmErrors()
        g_check_i = 0
        
        text_entries = []
        redo_boxes   = []
        print "\t- Beginning parameter analysis"
        #### Pulls
        for p in xrange(n_params):
            i   = n_params - (p + 1)
            pre = pdata[p]['prefit']
            fit = pdata[p]['fit']
            tp  = pdata[p]['type']
            seen_types.add(tp)
            if pdata[p]['type'] != 'Unconstrained':
                pre_err_hi = (pre[2] - pre[1])
                pre_err_lo = (pre[1] - pre[0])

                pull = fit[1] - pre[1]
                pull = (pull/pre_err_hi) if pull >= 0 else (pull/pre_err_lo)
                pull_hi = fit[2] - pre[1]
                pull_hi = (pull_hi/pre_err_hi) if pull_hi >= 0 else (pull_hi/pre_err_lo)
                pull_hi = pull_hi - pull
                pull_lo = fit[0] - pre[1]
                pull_lo = (pull_lo/pre_err_hi) if pull_lo >= 0 else (pull_lo/pre_err_lo)
                pull_lo =  pull - pull_lo

                g_pulls.SetPoint(i, pull, float(i) + 0.5)
                g_pulls.SetPointError(
                    i, pull_lo, pull_hi, 0., 0.)
            else:
                # Hide this point
                g_pulls.SetPoint(i, 0., 9999.)
                y1 = r.gStyle.GetPadBottomMargin()
                y2 = 1. - r.gStyle.GetPadTopMargin()
                x1 = r.gStyle.GetPadLeftMargin()
                h = (y2 - y1) / float(n_params)
                y1 = y1 + ((float(i)+0.5) * h)
                x1 = x1 + (1 - pads[0].GetRightMargin() -x1)/2.
                s_nom, s_hi, s_lo = GetRounded(fit[1], fit[2] - fit[1], fit[1] - fit[0])
                text_entries.append((x1, y1, '%s^{#plus%s}_{#minus%s}' % (s_nom, s_hi, s_lo)))
                redo_boxes.append(i)
             
            for iP in range(npois):
                g_impacts_hi_list[iP].SetPoint(i, 0, float(i) + 0.5)
                g_impacts_lo_list[iP].SetPoint(i, 0, float(i) + 0.5)
            
            
            imp_list = []
            for nam in poiDict:
                imp_list.append(pdata[p][nam])
                
            for iP in range(npois):
                g_impacts_hi_list[iP].SetPointError(i, 0, imp_list[iP][2] - imp_list[iP][1], 0.5, 0.5)
                g_impacts_lo_list[iP].SetPointError(i, imp_list[iP][1] - imp_list[iP][0], 0, 0.5, 0.5)
                max_impact_list[iP] = max(
                    max_impact_list[iP], abs(imp_list[iP][1] - imp_list[iP][0]), abs(imp_list[iP][2] - imp_list[iP][1]))
            max_impact = max(max_impact_list)
                
            col = nuisanceColours.get(tp, 2)
            if colour_groups is not None and len(pdata[p]['groups']) >= 1:
                for p_grp in pdata[p]['groups']:
                    if p_grp in colour_groups:
                        col = colour_groups[p_grp]
                        break
            h_pulls.GetYaxis().SetBinLabel(
                #i + 1, ('#color[%i]{%s}'% (col, vl.SysNameTranslator[pdata[p]['name'].encode('utf-8')])))
                i + 1, ('#color[%i]{%s}'% (col, pdata[p]['name'].encode('utf-8'))))

        # Style and draw the pulls histo
        plot.Set(h_pulls.GetXaxis(), TitleSize = xaxistitlesize, LabelSize = 0.015, TitleOffset=xaxistitleoffset-0.09, Title='(#hat{#theta}-#theta_{0})/#Delta#theta')
        plot.Set(h_pulls.GetYaxis(), LabelSize = label_size, TickLength=0.0)
        h_pulls.GetYaxis().LabelsOption('v')
        h_pulls.Draw()

        for i in redo_boxes:
            newbox = boxes[i].Clone()
            newbox.Clear()
            newbox.SetY1(newbox.GetY1()+0.005)
            newbox.SetY2(newbox.GetY2()-0.005)
            newbox.SetX1(r.gStyle.GetPadLeftMargin()+0.001)
            newbox.SetX2(0.7-0.001)
            newbox.Draw()
            boxes.append(newbox)
        latex = r.TLatex()
        latex.SetNDC()
        latex.SetTextFont(42)
        latex.SetTextSize(0.02)
        latex.SetTextAlign(22)
        for entry in text_entries:
            latex.DrawLatex(*entry)

        # Go to the other pad and draw the impacts histo
        h_impacts_list = []
        for iP in range(npois):
            pads[iP + 1].cd()
            if max_impact == 0.: max_impact = 1E-6  # otherwise the plotting gets screwed up
            h_impacts_list.append(r.TH2F("impacts_" + str(iP), 
                                         "impacts_" + str(iP), 
                                         6, 
                                         -max_impact * 1.1, 
                                         max_impact* 1.1, 
                                         n_params, 
                                         0, 
                                         n_params))
            plot.Set(h_impacts_list[-1].GetXaxis(), 
                     LabelSize  = 0.015, 
                     TitleSize  = xaxistitlesize, 
                     TitleOffset=xaxistitleoffset,
                     Ndivisions = 505, 
                     Title      = '#Delta#hat{#mu_{%s}}'%(iP))
            plot.Set(h_impacts_list[-1].GetYaxis(), 
                     LabelSize  = 0, 
                     TickLength = 0.0)
            h_impacts_list[-1].Draw()
        print len(pads)

        # Back to the first pad to draw the pulls graph
        pads[0].cd()
        plot.Set(g_pulls, 
                 MarkerSize = 0.8, 
                 LineWidth  = 2)
        g_pulls.Draw('PSAME')

        # And back to the second pad to draw the impacts graphs
        alpha  = 0.7
        method = 'default'
        if 'method' in data and data['method'] in lo_colour:
            method = data['method']
        
        for iP in range(npois):
            pads[iP + 1].cd()
            g_impacts_hi_list[iP].SetFillColor(plot.CreateTransparentColor(hi_colour[method], alpha))
            g_impacts_hi_list[iP].Draw('2SAME')
            g_impacts_lo_list[iP].SetFillColor(plot.CreateTransparentColor(lo_colour[method], alpha))
            g_impacts_lo_list[iP].Draw('2SAME')
            pads[iP + 1].RedrawAxis()
            

        legend = r.TLegend(0.02, 0.02, 0.30, 0.04, '', 'NBNDC')
        legend.SetNColumns(3)
        legend.AddEntry(g_pulls, 'Pull', 'LP')
        legend.AddEntry(g_impacts_hi_list[0], '+1#sigma Impact', 'F')
        legend.AddEntry(g_impacts_lo_list[0], '-1#sigma Impact', 'F')
        legend.Draw()

        leg_width = pads[0].GetLeftMargin() - 0.01
        if colour_groups is not None:
            legend2 = r.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
            legend2.SetNColumns(2)
            for name, h in colour_group_hists.iteritems():
#                legend2.AddEntry(h, vl.SysNameTranslator[name], 'F')
                legend2.AddEntry(h, name, 'F')
            legend2.Draw()
        elif len(seen_types) > 1:
            legend2 = r.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
            legend2.SetNColumns(2)
            for name, h in colour_hists.iteritems():
                if name == 'Unrecognised': continue
                legend2.AddEntry(h, name, 'F')
            legend2.Draw()

        plot.DrawCMSLogo(pads[0], 'CMS', cms_label, 0, 0.27, 0.0, 0.00, cmsTextSize = 0.5)
        s_nom_list = []; s_hi_list = []; s_lo_list = []
        
        for iP in range(npois):
            s_nom, s_hi, s_lo = GetRounded(poiDict["r_TTW_%s_bin%d"%(varName,iP)]["fit"][1], 
                                           poiDict["r_TTW_%s_bin%d"%(varName,iP)]["fit"][2] - poiDict["r_TTW_%s_bin%d"%(varName,iP)]["fit"][1], 
                                           poiDict["r_TTW_%s_bin%d"%(varName,iP)]["fit"][1] - poiDict["r_TTW_%s_bin%d"%(varName,iP)]["fit"][0])
            s_nom_list.append(s_nom); s_hi_list.append(s_hi); s_lo_list.append(s_lo);
            
        if not doBlind:
            for iP in range(npois):
                plot.DrawTitle(pads[iP + 1], '#hat{#mu_{%s}} = %s^{#plus%s}_{#minus%s}%s' % (
                    iP, s_nom_list[iP], s_hi_list[iP], s_lo_list[iP],
                    '' if units is None else ' ' + units), 3, 0.27, 0.3)

        extra = ''
        if page == 0:
            extra = '('
        if page == n - 1:
            extra = ')'
        canv.Print('{path}/{nam}.pdf{ex}'.format(path = outputpath, nam = outputname, ex = extra))
    return


def makeImpacts(task):
    inpath, varName, ncores, pretend, verbose, extra, doobs, doblind, regName = task

    print '\n> Creating impacts for variable', varName,regName
    bins_detector = eval(all_vars[(varName,regName)].CATBINS)
    ndetectorbins   = len(bins_detector) - 1
    bins_particle = eval(all_vars[(varName,regName)].CATBINS_Gen)
    nparticlebins   = len(bins_particle) - 1

    thepois = ",".join( ["r_TTW_%s_bin%d"%(varName,i) for i in range(nparticlebins)] )


    asimov_ = "--setParameters "
    asimov_ += ",".join( ["r_TTW_%s_bin%d=1"%(varName,idx) for idx in range(nparticlebins)])


    if not doobs:
        asimov_ +=  " -t -1 "


    firstcomm = comm1.format(ncores = ("--parallel " + str(ncores)) if ncores else "",
                             asimov = asimov_,
                             incard = "../ws_"+varName+"_"+regName+'.root',
                             outdir = "./"+regName,
                             var    = varName,
                             extra  = extra,
                             prefix = varName+"_"+regName,
                             pois   = thepois,
    )

    if verbose:
        print "First command:", firstcomm, "\n"

    if not pretend  and  firststepbatch:
        if not os.path.exists(inpath + "/impacts_"+regName):
               os.system("mkdir "+inpath + "/impacts_"+regName)
        out_file = open(inpath + "/impacts_"+regName+"/impact_first_step.sh", "w")
        outstat = os.system("cd " + inpath + "/impacts_"+regName+"; " +"sbatch -p batch --wrap '" +firstcomm + " ' "+"; cd -")
        queue = "batch"
        comb = "~/Combine_repo/CMSSW_10_2_13/src/"
        submit = 'cd {foldtorun} && {command} '
        out_file.write(JOB_PREFIX)
        out_file.write((submit.format(combinerepo=comb,foldtorun=inpath + "/impacts_"+regName,command=firstcomm)))
        out_file.close()
        os.chmod(inpath + "/impacts_"+regName+"/impact_first_step.sh", 0o777)
        if outstat:
            raise RuntimeError("FATAL: first command failed to execute for variable {v}.".format(v = varName))

    if not pretend  and  firststep:
        if not os.path.exists(inpath + "/impacts_"+regName):
               os.system("mkdir "+inpath + "/impacts_"+regName)
        outstat = os.system("cd " + inpath + "/impacts_"+regName+"; "  +firstcomm +"; cd -")
        #print("sbatch -p batch --wrap '" +firstcomm + " ' ")
        if outstat:
            raise RuntimeError("FATAL: first command failed to execute for variable {v}.".format(v = varName))


    secondcomm = comm2.format(ncores = ("--parallel " + str(ncores)) if ncores else "",
                             asimov = asimov_,
                             incard = "../ws_"+varName+"_"+regName+'.root',
                             outdir = "./"+regName,
                             var    = varName,
                             extra  = extra,
                             prefix = varName+"_"+regName,
                             pois   = thepois,
    )

    if verbose:
        print "Second command:", secondcomm, "\n"

    if not pretend  and  secondstep:
        outstat = os.system("cd " + inpath + "/impacts_"+regName+"; " + secondcomm + "; cd -")
        if outstat:
            raise RuntimeError("FATAL: second command failed to execute for variable {v}.".format(v = varName))
    thirdcomm = comm3.format(ncores = ("--parallel " + str(ncores)) if ncores else "",
                             asimov = asimov_,
                             incard = "../ws_"+varName+"_"+regName+'.root',
                             outdir = "./",
                             var    = varName,
                             extra  = extra,
                             prefix = varName+"_"+regName,
                             pois   = thepois,
    )

    if verbose:
        print "Third command:", thirdcomm, "\n"

    if not pretend and thirdstep:
        print("cd " + inpath + "/impacts_"+regName+"; " + thirdcomm + "; cd -")
        outstat = os.system("cd " + inpath + "/impacts_"+regName+"; " + thirdcomm + "; cd -")
        if outstat:
            raise RuntimeError("FATAL: third command failed to execute for variable {v}.".format(v = varName))

    
        plotImpacts(inpath+"/impacts_"+regName+ "/impacts{v}.json".format(v = varName+"_"+regName), "impacts{v}".format(v = varName+"_"+regName), inpath, nparticlebins, doblind, varName,regName)
        print '\n> Variable', varName, "' impacts produced.\n"
        return



if __name__ == '__main__':
    
    r.gROOT.SetBatch(True)
    print "===== Fitting procedure with some uncertainty profiling\n"
    parser = argparse.ArgumentParser(usage = "python nanoAOD_checker.py [options]", description = "Checker tool for the outputs of nanoAOD production (NOT postprocessing)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inpath',     '-i', metavar = 'inpath',     dest = "inpath",   required = False, default = "./temp/differential/")
    parser.add_argument('--variable',   '-v', metavar = 'variable',   dest = "variable", required = False, default = "all")
    parser.add_argument('--region',     '-r', metavar = 'region',     dest = "region",   required = False, default = "2lss")
    parser.add_argument('--extraArgs',  '-e', metavar = 'extra',      dest = "extra",    required = False, default = "")
    parser.add_argument('--nthreads',   '-j', metavar = 'nthreads',   dest = "nthreads", required = False, default = 0, type = int)
    parser.add_argument('--pretend',    '-p', action  = "store_true", dest = "pretend",  required = False, default = False)
    parser.add_argument('--verbose',    '-V', action  = "store_true", dest = "verbose",  required = False, default = False)
    parser.add_argument('--doObserved', '-O', action  = "store_true", dest = "doobs",    required = False, default = False)
    parser.add_argument('--blindSignalStrength','-b',action="store_true",dest="blindmu", required = False, default = False)
    parser.add_argument('--initialFit',    '-I',action="store_true",dest="firststep", required = False, default = False)
    parser.add_argument('--initialFitBatch',    '-Ib',action="store_true",dest="firststepbatch", required = False, default = False)
    parser.add_argument('--FitbyFit',    '-M',action="store_true",dest="secondstep", required = False, default = False)
    parser.add_argument('--lastPart',    '-F',action="store_true",dest="thirdstep", required = False, default = False)


    args     = parser.parse_args()
    nthreads = args.nthreads
    pretend  = args.pretend
    inpath   = args.inpath
    varName  = args.variable
    regName  = args.region
    verbose  = args.verbose
    extra    = args.extra
    doobs    = args.doobs
    doblind  = args.blindmu
    ncores   = args.nthreads
    firststep = args.firststep
    firststepbatch = args.firststepbatch
    secondstep = args.secondstep
    thirdstep = args.thirdstep


    task=inpath, varName, ncores, pretend, verbose, extra, doobs, doblind,regName
    makeImpacts(task)
