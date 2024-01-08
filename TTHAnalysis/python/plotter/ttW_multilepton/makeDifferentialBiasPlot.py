""" Macro to plot differential distributions """
import ROOT as r 
import re
import collections
import math 
import os,sys
from optparse import OptionParser
from copy import deepcopy
from collections import OrderedDict
from differential_variables import all_vars

r.gROOT.ProcessLine(".x tdrstyle.cc")
r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)
r.gROOT.SetBatch(True)

# ============== Some predefined values =============
lumis = {
    "2016APV" : 16.8, 
    "2016" : 19.5,
    "2017"  : 41.4,
    "2018" : 59.7
}

years = ["2016APV", "2016", "2017", "2018"]
# ===================================================

def arg_parser():
    parser = OptionParser(description="Live free or die")
    
    parser.add_option("--unfold-signal", "-u", dest = "unfold_signal", nargs = 2, 
                      help="Unfolding sample. Takes two inputs: name for legend and path to cards")
    
    parser.add_option("--add-signal", "-a", dest = "add_signal", nargs = 2, action = "append", 
                      help="""Additional signal sample to plot. Can be specified multiple times. Takes also
                      two inputs: name for legend and path to card. """)
    
    parser.add_option("--variable", "-x", dest = "variable", default = "njets", 
                      help="Variable to plot.")
    
    parser.add_option("--norm", "-w", dest = "norm", default = False, action = "store_true",
                    help="Normalize to fiducial cross section or not.")
    
    parser.add_option('--region', "-r", dest = "region", default = "2lss",
                      help='Analysis region (2lss or 3l)')
    return parser.parse_args()

def get_histo(inpath, variable, region, binname = "x_TTW_inclusive", name = ""):
    """ Retrieve the truth info for a given sample """
    
    gencard = "ttW_{region}_0tau_Gen_{variable}_{year}.root"
    files = []
    for year in years:
        substitute = {
            "variable" : variable,
            "region" : region,
            "year" : year
        }
        files.append( os.path.join(inpath, gencard.format(**substitute)) )    
    
    # Open first file and then add the remaining ones
    tf0 = r.TFile.Open( files[0], "READ" )
    h0 = deepcopy(tf0.Get(binname).Clone("x_TTW_{name}".format(name = name)))
    tf0.Close()
    for iy, year in enumerate(years[1:]):
        tf = r.TFile.Open( files[iy + 1], "READ")
        h = deepcopy(tf.Get(binname))
        h0.Add(h)
        tf.Close()
    
    # Normalize to lumi
    h0.Scale( 1/ sum( [lumis[year] for year in years]) )
    return h0

def get_asimov(reference, fitResult, normDataToFid):
    """ This function builds the unfolded data by scaling
    a reference histogram.
    """
    nPoints = reference.GetNbinsX()
    results = {}
    poinames = []

    count = 0
    for v in fitResult.floatParsFinal():
        if "r_TTW" in v.GetName():
            count += 1
            results[v.GetName()] = [ v.getVal(), abs(v.getErrorLo()), v.getErrorHi(), v.getError() ]
            poinames.append(v.GetName())
            if count == nPoints: break

    pois_0 = results.keys()
    
    #order pois by bin number
    index = []
    for p in pois_0:
        i = re.sub(r'\D', "", p) #remove all items which are not numbers
        index.append(int(i))
        
    pois = [p for _,p in sorted(zip(index,pois_0))]
    
    diffhisto = deepcopy(reference.Clone("diffhisto"))
    for bin in range(1,reference.GetNbinsX()+1):
        values = results[pois[bin-1]]
        nom   = values[0]
        upvar = values[2]
        dnvar = values[1]
        unc   = values[3]
        
        diffhisto.SetBinContent(bin,nom*reference.GetBinContent(bin)) #Histo with differential cross section
        diffhisto.SetBinError(bin,(unc)*reference.GetBinContent(bin))
    
    
    if normDataToFid:
        # 1. Get the covariance matrix
        poiList = r.RooArgList('poiList')
        for poi in pois:
            variation = w.var(poi)
            poiList.add(variation)
        cov = fitResult.reducedCovarianceMatrix(poiList)
        xsec_fid = sum(results[pois[bin]][0]*reference.GetBinContent(bin+1) for bin in range(reference.GetNbinsX()))
        diffhisto = UncPropagation(diffhisto, xsec_fid, cov, len(pois))
   
    return diffhisto

def UncPropagation(h_dSigma,fiducial, corr,npois ):
   """
   h_dSigma: histo with dsigma with error 
   fiducial: xsec fiducial
   corr: correlation matrix  
   """
   hnormalized = h_dSigma.Clone("hnormalized")
   fid_unc = r.TMath.Sqrt(sum(corr[i-1][j-1] for i in range(1,npois+1) for j in range(1,npois+1)  ))
   for bin in range(1,h_dSigma.GetNbinsX()+1):
       corr_i_j = sum(corr[bin-1][j-1] for j in range(1,npois+1))
       variance = h_dSigma.GetBinError(bin)**2/(fiducial**2) + ((fid_unc**2)*h_dSigma.GetBinContent(bin)**2)/(fiducial**4) - (2*h_dSigma.GetBinContent(bin)* corr_i_j)/(fiducial**3)
       uncertainty = r.TMath.Sqrt(variance)
   

       hnormalized.SetBinContent(bin,  h_dSigma.GetBinContent(bin)/fiducial)
       hnormalized.SetBinError(bin,  uncertainty)
   return hnormalized

def get_graph(h):
    """ Compute a graph from a reference histogram """
    gr = r.TGraphAsymmErrors( h.GetNbinsX() )
    for ibin in range(1, h.GetNbinsX() + 1):
        xval=h.GetBinCenter(ibin) 
        gr.SetPoint(ibin-1, xval, h.GetBinContent(ibin))
        gr.SetPointEYhigh(ibin-1, h.GetBinError(ibin))
        gr.SetPointEYlow(ibin-1,  h.GetBinError(ibin))
        
    # Remove 0
    for ip in range(gr.GetN()):
        if gr.GetY()[ip] == 0: gr.RemovePoint(ip)
    return gr

def get_ratio(num, den):
    """ Compute the ratio between a graph (num) and a histogram (den) """
    ratio = deepcopy(num.Clone(num.GetName() + "_ratio"))
    for i in range(ratio.GetN()):
        x    = ratio.GetX()[i]
        div  = den.GetBinContent(den.GetXaxis().FindBin(x))
        ratio.SetPoint(i, x, ratio.GetY()[i]/div if div > 0 else 0)
        ratio.SetPointError(i, ratio.GetErrorXlow(i), ratio.GetErrorXhigh(i), 
                    ratio.GetErrorYlow(i)/div  if div > 0 else 0, 
                    ratio.GetErrorYhigh(i)/div if div > 0 else 0) 
    return ratio

def doShadedUncertainty(h,unc_dic,relative = False):
    xaxis = h.GetXaxis()
    points = []; errors = []; 
    for i in range(h.GetNbinsX()):
        N = h.GetBinContent(i+1)
        dN = h.GetBinError(i+1)
        if N == 0 and (dN == 0 or relative): continue
        x = xaxis.GetBinCenter(i+1)

        EXhigh, EXlow = (xaxis.GetBinUpEdge(i+1)-x, x-xaxis.GetBinLowEdge(i+1))

        uncUp=[]
        uncDn =[]

        for key in unc_dic:
            uncUp.append( unc_dic[key][0].GetBinContent(i+1)-N)
            uncDn.append( unc_dic[key][1].GetBinContent(i+1)-N)

        uncUp_tot = r.TMath.Sqrt(sum([uncsource**2 for uncsource in uncUp]))
        uncDn_tot = r.TMath.Sqrt(sum([uncsource**2 for uncsource in uncDn]))
        EYlow = r.TMath.Sqrt(dN**2 +uncDn_tot**2)
        EYhigh = r.TMath.Sqrt(dN**2 +uncUp_tot**2)

        if relative:
            errors.append( (EXlow,EXhigh,EYlow/N,EYhigh/N) )
            points.append( (x,1) )
        else:
            errors.append( (EXlow,EXhigh,EYlow,EYhigh) )
            points.append( (x,N) )
        
        #print( ">> Bin: %d -- (%s) Before:"%(i, h.GetName()), "Nom content: %3.4f"%N, "Error content: %3.4f"%points[-1][1], "Error unc: %3.4f"%uncUp_tot) 
        #for key in unc_dic:
        #    print("    o %s: nominal: %3.4f variation: %3.4f error = %3.4f"%(key, N, unc_dic[key][0].GetBinContent(i+1), unc_dic[key][0].GetBinContent(i+1)-N))


    ret = deepcopy(r.TGraphAsymmErrors(len(points)))
    ret.SetName(h.GetName()+"_errors")
    for i,((x,y),(EXlow,EXhigh,EYlow,EYhigh)) in enumerate(zip(points,errors)):
        ret.SetPoint(i, x, y)
        ret.SetPointError(i, EXlow, EXhigh, EYlow, EYhigh)

    ret.SetFillStyle(3244)
    ret.SetFillColor(1)
    ret.SetMarkerStyle(0)

    ret.Draw("PE2 SAME")
    return ret

def doSpam(text,x1,y1,x2,y2,align=12,fill=False,textSize=0.033,_noDelete={}):
    cmsprel = r.TPaveText(x1,y1,x2,y2,"NBNDC")
    cmsprel.SetTextSize(textSize)
    cmsprel.SetFillColor(0)
    cmsprel.SetFillStyle(1001 if fill else 0)
    cmsprel.SetLineStyle(2)
    cmsprel.SetLineColor(0)
    cmsprel.SetTextAlign(align)
    cmsprel.SetTextFont(42)
    cmsprel.AddText(text)
    cmsprel.Draw("same")
    _noDelete[text] = cmsprel; ## so it doesn't get deleted by PyROOT                                                                                                   
    return cmsprel

def doLegend(entries, coords, corner="TR",legWidth=0.18,textSize = 0.027):
    nentries = len(entries)
    x1, y1, x2, y2 = coords
    leg = r.TLegend(x1,y1,x2,y2)
    leg.SetFillColor(0)
    leg.SetShadowColor(0)
    leg.SetTextFont(42)
    leg.SetTextSize(textSize)
    leg.SetNColumns(1)
    leg.SetBorderSize(0)
    
    for i in range(0,nentries):
        leg.AddEntry(entries[i][0],entries[i][1],entries[i][2])
    
    ## assign it to a global variable so it's not deleted
    global legend_
    legend_ = leg 
    return leg
    
if __name__ == "__main__":
    # ---- Unpack parser options
    opts, args = arg_parser()
    unfold_signal = opts.unfold_signal
    additional_signals = opts.add_signal if opts.add_signal else []
    variable = opts.variable
    region = opts.region
    normDataToFid = opts.norm
    
    all_signals = [unfold_signal] + [addsignal for addsignal in additional_signals]
    observable = all_vars[(variable, region)]
    bins = observable.CATBINS_Gen
    bins_list = [float(ibin) for ibin in bins.replace("[", "").replace("]", "").split(",")]
    
    
    # ---- Print some summary
    print(" ---- Considering the following settings: ")
    print("   o Region: {} ".format(region))
    print("   o Unfolded signal ({}): {} ".format(unfold_signal[0], unfold_signal[1]))
    for additional in additional_signals:
        print("   o Additional signal ({}): {} ".format(additional[0], additional[1]))
    print("   o Variable: {}".format(variable))
    print("     + Bins: " + observable.CATBINS_Gen)
    print(" ---------------------------------------- ")
    
    
    # =========== Get all the inputs =========== # 
    # 1. Get the truth histograms + variations
    histos = {}
    theounc = ["_CMS_ttWl_thu_shape_ttW","_FSR","_ISR_ttW"]
    for iS, signal in enumerate(all_signals):
        signal_name = signal[0]
        cards = signal[1]
        binname = "x_TTW_inclusive" if signal_name == "nominal" else "x_TTW_%s_inclusive"%signal_name
        # Save the main histograms
        histos[signal_name] = {}
        histos[signal_name]["nominal"] = get_histo( cards, variable, region, binname = binname, name = signal_name )
        # Save the variated histograms
        uncs = {}
        for unc in theounc:
            hUp = get_histo( cards, variable, region, binname = binname + unc  + "Up", name = signal_name + "Up" )
            hDn = get_histo( cards, variable, region, binname = binname + unc  + "Down", name = signal_name + "Down" )     
            if normDataToFid: # Normalize also the MC by its fiducial xsec
                hUp.Scale( 1/hUp.Integral() )
                hDn.Scale( 1/hDn.Integral() )
            uncs[unc] = [hUp, hDn]
        histos[signal_name]["uncs"] = uncs
    

    # Check normalization
    if not normDataToFid:
        eft = histos[unfold_signal[0]]["nominal"]
        qcd = histos[additional_signals[0][0]]["nominal"]
        #print(eft.Integral(), qcd.Integral(), eft.Integral()/qcd.Integral())
        eft.Scale(eft.Integral()/qcd.Integral())
        for unc in theounc:
            eftVar = histos[unfold_signal[0]]["uncs"][unc]
            histos[unfold_signal[0]]["uncs"][unc][0].Scale(eft.Integral()/qcd.Integral())
            histos[unfold_signal[0]]["uncs"][unc][1].Scale(eft.Integral()/qcd.Integral())

    # 2. Get the fit results which are stored in the same path as the unfolded signal cards.
    fits = {
        "total"  : "fitDiagnosticsnominal_{variable}_{region}.root",
        "mcstat" : "fitDiagnosticsfreezing_{variable}_{region}.root",
        "stat"   : "fitDiagnosticsfreezing_all_{variable}_{region}.root"
    }
    fit_results = {}
    for fitname, fitpath in fits.items():
        fullFitPath = os.path.join( unfold_signal[1], fitpath.format(variable = variable, region = region))
        tf = r.TFile.Open(fullFitPath)
        fitResult = deepcopy( tf.Get("fit_s") )
        fit_results[fitname] = deepcopy(fitResult)
        tf.Close()

    # 3. Open the workspace. Which is also stored in the same path as the unfolded signal cards.
    wsname = "ws_{variable}_{region}.root"
    wspath = os.path.join( unfold_signal[1], wsname.format(variable = variable, region = region) )
    tws = r.TFile.Open(wspath)
    w = tws.Get("w")
    
    # =========== Build the objects to plot =========== #
    toPlot = {}
    
    # Data (blinded case): build the asimov data by scaling with the expected cross section
    h_data = get_asimov(histos[additional_signals[0][0]]["nominal"], fit_results["total"], normDataToFid)
    gr_data = get_graph(h_data)
    toPlot["data"] = {"upper" : gr_data}

    # MC
    for signalName, signalDict in list(histos.items()):
        hNom = signalDict["nominal"]
        uncs = signalDict["uncs"]
        if normDataToFid: # Normalize also the MC by its fiducial xsec
            hNom.Scale( 1 / hNom.Integral() )
        ratio = get_ratio(gr_data, hNom)
        error = doShadedUncertainty(hNom, uncs)
        
        #for ibin in range(hNom.GetNbinsX()):
        #    print( "(%s) After:"%signalName, "Nom content: %3.4f"%hNom.GetBinContent(ibin+1), "Error content: %3.4f"%error.GetErrorYlow(ibin), "Error unc: %3.4f"%error.GetErrorYhigh(ibin)) 
        toPlot[signalName] = {"upper" : hNom, "ratio" : ratio, "unc" : error}
        #print(" ----- ")
        
      
    # =========== PLOT =========== #
    # -- Spams 
    spamCMS = doSpam('#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}',  0.16, .955,0.6, .995, align=12, textSize=0.033*1.4)
    spamLUMI = doSpam('%3.0f fb^{-1} (13 TeV)'%(sum( [lumis[year] for year in years])),  0.67, .955,0.99, .995, align=12, textSize=0.033*1.4)
    
    # -- Load some cosmetics
    from ttW_beauty import frame_cosmetics, process_cosmetics_bias
    frame_cosm = frame_cosmetics[variable]
    
    # -- Canvas    
    tokeep=[]
    topSpamSize=1.2
    plotformat = (frame_cosm["canvas_sizeX"], frame_cosm["canvas_sizeY"])
    c1 = r.TCanvas("_canvas", '', plotformat[0], plotformat[1])
    
    p1 = r.TPad("pad1","pad1",0, 0.30, 1, 1)
    p1.SetTopMargin(p1.GetTopMargin()*topSpamSize)
    p1.SetBottomMargin(0)
    p1.Draw()
    
    p2 = r.TPad("pad2","pad2",0, 0, 1, 0.30)
    p2.SetTopMargin(0)
    p2.SetBottomMargin(0.3)
    p2.SetFillStyle(0)
    p2.Draw()
    
    # ------ UPPER CANVAS ------ #
    p1.cd()
    frame=r.TH1F("frame","",1, bins_list[0], bins_list[-1])
    frame.GetXaxis().SetTitleFont(42)
    frame.GetXaxis().SetTitleSize(0.06)
    frame.GetXaxis().SetTitleOffset(0.07)
    frame.GetXaxis().SetLabelFont(42)
    frame.GetXaxis().SetLabelSize(0.06)
    frame.GetXaxis().SetLabelOffset(0.007)
    frame.GetYaxis().SetTitleFont(42)
    frame.GetYaxis().SetTitleSize(0.12)
    frame.GetYaxis().SetLabelFont(42)
    frame.GetYaxis().SetLabelSize(0.12)
    titleY = "#frac{d#sigma}{d %s}"%frame_cosm["frame_titleY"]
    titleY = "(1/#sigma_{f})" + titleY if normDataToFid else titleY
    frame.GetYaxis().SetTitle(titleY)
    frame.GetXaxis().SetNdivisions(510)
    frame.GetXaxis().SetLabelOffset(999) ## send them away
    frame.GetXaxis().SetTitleOffset(999) ## in outer space
    frame.GetYaxis().SetTitleSize(0.06)
    frame.GetYaxis().SetTitleOffset(1.2)
    frame.GetYaxis().SetLabelSize(0.05)
    frame.GetYaxis().SetLabelOffset(0.007)
    frame.Draw()
    
    # ------ LOWER CANVAS ------ #
    p2.cd()
    frameratio=r.TH1F("ratioframe","",1, bins_list[0], bins_list[-1])
    frameratio.GetXaxis().SetTitle(frame_cosm["frameratio_titleX"])
    frameratio.GetYaxis().SetTitle(frame_cosm["frameratio_titleY"])
    frameratio.SetBinError(1,0)
    frameratio.SetBinContent(1,1)
    frameratio.GetXaxis().SetTitleFont(42)
    frameratio.GetXaxis().SetTitleSize(0.14)
    frameratio.GetXaxis().SetTitleOffset(0.98)
    frameratio.GetXaxis().SetLabelFont(42)
    frameratio.GetXaxis().SetLabelSize(0.1)
    frameratio.GetXaxis().SetLabelOffset(0.015)
    frameratio.GetYaxis().SetNdivisions(505)
    frameratio.GetYaxis().SetTitleFont(42)
    frameratio.GetYaxis().SetTitleSize(0.14)
    #frameratio.GetXaxis().SetTitleOffset(0.014)
    offset = 0.62
    frameratio.GetYaxis().SetTitleOffset(offset)
    frameratio.GetYaxis().SetLabelFont(42)
    frameratio.GetYaxis().SetLabelSize(0.1)
    frameratio.GetYaxis().SetLabelOffset(0.01)
    frameratio.GetYaxis().SetDecimals(True) 
    frameratio.Draw()
    
    # Now plot everything
    legend_entries = []
    maxY = 0

    # Plot the data
    p1.cd()

    for plotname, plots in toPlot.items():
        if plotname == "data": continue
        maxY = max(maxY, plots["upper"].GetMaximum())
        plots["upper"].SetLineColor( process_cosmetics_bias[plotname]["color"] )
        plots["ratio"].SetMarkerColor( process_cosmetics_bias[plotname]["color"] )
        plots["ratio"].SetLineColor( process_cosmetics_bias[plotname]["color"] )
        plots["ratio"].SetMarkerSize( 1 )
        plots["unc"].SetFillColor( process_cosmetics_bias[plotname]["color"] )
            
        p1.cd()
        plots["upper"].Draw("hist same")
        plots["unc"].Draw( "e2 same" )

        p2.cd()
        plots["ratio"].Draw("p same")
        legend_entries.append( [plots["upper"], process_cosmetics_bias[plotname]["legend"], "l"] )
    
    p1.cd()
    gr_data = toPlot["data"]["upper"]
    gr_data.Draw("pe same")
    legend_entries.append( [gr_data, "Data", "p"])
    
    frame.GetYaxis().SetRangeUser(0, maxY*frame_cosm["frame_scaleY"])
    frameratio.GetYaxis().SetRangeUser( 1-frame_cosm["frameratio_range"], 1+frame_cosm["frameratio_range"] )
    p1.cd()
    leg=doLegend(legend_entries, frame_cosm["legend_coords"])
    leg.Draw("same")
    
    c1.SaveAs("prueba.png")