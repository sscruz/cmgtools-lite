import ROOT as r 
import re
import collections
import math 
import os,sys
import numpy as np
r.gROOT.ProcessLine(".x tdrstyle.cc")
r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)
r.gROOT.SetBatch(True)

lumi = 16.8+19.5+41.4+59.7#use the lumi used to normalized the gen histos (fb-1)

#Inputs: folder region (2lss 3l) variable
folder = sys.argv[1]
region = sys.argv[2]
var = sys.argv[3]

#Dictionary with allowed input varaibles 
varname = {"lep1_pt":("p_{T} (lep1)"),"lep2_pt":("p_{T} (lep2)"),"lep1_eta":("#eta (lep1)"),"lep2_eta":("#eta (lep2)"),"njets":("N Jet"),"njets_7bins":("N Jet"),"nbjets":("N b-tag Loose"),"jet1_pt":("p_{T} (jet)"),"jet1_eta":("|#eta| (jet1)"),"deta_llss":("#Delta #eta (ll)"),"HT":("HT"),"dR_ll":("#Delta R (ll)"),"max_eta":("max(#eta) (ll)"), "pt3l": ("p_{T} 3l"), "m3l":("m_{3l}"),"dR_lbmedium":(" #Delta R (l bmedium)"),"mindr_lep1_jet25":("min #Delta R (lj)"),"dR_lbloose":(" #Delta R (l bloose)"),"jet2_pt":(" p_{T} (jet 2)"),"jet2_eta":(" |#eta| (jet 2)"),"bLooseLeadingJet_eta":(" |#eta| (bLoose 1)"),"bLooseLeadingJet_pt":(" p_{T}  (bLoose 1)"),"bMediumLeadingJet_eta":(" |#eta| (bMedium 1)"),"bMediumLeadingJet_pt":(" p_{T}  (bMedium 1)"),"sum_2lss_pt":(" p_{T}^{lep1}+p_{T}^{lep2}  "),"nbjets_medium":(" N b-tag medium ") ,"mll":(" m_ll ")  }



if var not in varname.keys():
   print("Variable not included, please add")

if "2lss" in region:
   region = "2lss"
   regioncard = "2lss_0tau"
   
elif "3l" in region:
   region = "3l"
   regioncard  = "3l_0tau"
GenInfo=folder+"/ttW_"+regioncard+"_Gen_"+var

#Get info needed from the fit
Fit = folder+"/fitDiagnosticsNoasimov_nominal_"+var+"_"+region+".root"
fit_st = folder+"/fitDiagnosticsNoasimov_freezing_"+var+"_"+region+".root"
ws = folder+"/ws_"+var+"_"+region+".root"

#and open it
if not os.path.isfile(ws):
   raise RuntimeError("FATAL: file {f} does not exist. Please create workspace!".format(f = ws))
tws = r.TFile.Open(ws)
w = tws.Get("w")

if not os.path.isfile(str(Fit)):
   raise RuntimeError("FATAL: file {f} does not exist. Please run fit!".format(f = str(Fit)))
tf_fit = r.TFile.Open(str(Fit))

if not os.path.isfile(str(fit_st)):
   raise RuntimeError("FATAL: file {f} does not exist. Please run fit for stats only!".format(f = str(fit_st)))
tf_fitst = r.TFile.Open(str(fit_st))

fitResult = tf_fit.Get('fit_s')
fitResult_stat = tf_fitst.Get('fit_s')
maxim = 0
maxY = 0

_noDelete={}

def Get_Genhisto(tf,tf1,tf2,tf3,name):
    print(name)
    reference1=tf.Get(name)
    reference2=tf1.Get(name)
    reference3=tf2.Get(name)
    reference4=tf3.Get(name)
 
    reference = reference1.Clone("reference"+name)
   
    reference.Add(reference2)
    reference.Add(reference3)
    reference.Add(reference4)
    print(reference1.GetBinContent(1),reference1.GetBinError(1))
    print(reference2.GetBinContent(1),reference2.GetBinError(1))
    print(reference3.GetBinContent(1),reference3.GetBinError(1))
    print(reference4.GetBinContent(1),reference4.GetBinError(1))
    print(reference.GetBinContent(1),reference.GetBinError(1))
    
    return reference

def doSpam(text,x1,y1,x2,y2,align=12,fill=False,textSize=0.033,_noDelete={}):
    cmsprel = r.TPaveText(x1,y1,x2,y2,"NBNDC");
    cmsprel.SetTextSize(textSize);
    cmsprel.SetFillColor(0);
    cmsprel.SetFillStyle(1001 if fill else 0);
    cmsprel.SetLineStyle(2);
    cmsprel.SetLineColor(0);
    cmsprel.SetTextAlign(align);
    cmsprel.SetTextFont(42);
    cmsprel.AddText(text);
    cmsprel.Draw("same");
    _noDelete[text] = cmsprel; ## so it doesn't get deleted by PyROOT                                                                                                   
    return cmsprel

def doLegend(entries, corner="TR",legWidth=0.18,textSize = 0.035):

        nentries = len(entries)
        height = (.15 + textSize*max(nentries-3,0))
        if corner == "TR":
            (x1,y1,x2,y2) = ( .85-legWidth, .9 - height, .90, .91)
        elif corner == "TC":
            (x1,y1,x2,y2) = (.5, .9 - height, .55+legWidth, .91)
        elif corner == "TL":
            (x1,y1,x2,y2) = (.2, .9 - height, .25+legWidth, .91)
        elif corner == "BR":
            (x1,y1,x2,y2) = (.85-legWidth, .16 + height, .90, .15)
        elif corner == "BC":
            (x1,y1,x2,y2) = (.5, .16 + height, .5+legWidth, .15)
        elif corner == "BL":
            (x1,y1,x2,y2) = (.2, .16 + height, .2+legWidth, .15)
        leg = r.TLegend(x1,y1,x2,y2)
        leg.SetFillColor(0)
        leg.SetShadowColor(0)
        leg.SetTextFont(42)
        leg.SetTextSize(textSize)
        for i in range(0,nentries):
            print(entries[i])
            leg.AddEntry(entries[i][0],entries[i][1],entries[i][2])
        leg.Draw()
        ## assign it to a global variable so it's not deleted
        global legend_
        legend_ = leg 
        return leg

def hypot(a,b):
    return math.sqrt(a**2+b**2)


def doShadedUncertainty(h,unc_list_up,unc_list_dn,lumi,relative = False):
      xaxis = h.GetXaxis()
      points = []; errors = []
      for i in xrange(h.GetNbinsX()):
            N = h.GetBinContent(i+1)/lumi;
            dNup = []
            dNdn = []
            for herr in unc_list_up:
                var = herr.GetBinContent(i+1)/lumi
                err  = (N-var)
                dNup.append(err)
            for herr in unc_list_dn:
                var = herr.GetBinContent(i+1)/lumi
                err  = (N-var)
                dNdn.append(err)
            if N == 0 and (dN == 0 or relative): continue
            x = xaxis.GetBinCenter(i+1);
            EYhigh = math.sqrt(sum(np.array(dNup)*np.array(dNup)))
            EYlow =math.sqrt(sum(np.array(dNdn)*np.array(dNdn)))
            EXhigh, EXlow = (xaxis.GetBinUpEdge(i+1)-x, x-xaxis.GetBinLowEdge(i+1))
            if relative:
                errors.append( (EXlow,EXhigh,EYlow/N,EYhigh/N) )
                points.append( (x,1) )
            else:
                errors.append( (EXlow,EXhigh,EYlow,EYhigh) )
                points.append( (x,N) )
      ret = r.TGraphAsymmErrors(len(points))
      print(type(ret))
      ret.SetName(h.GetName()+"_errors")
      for i,((x,y),(EXlow,EXhigh,EYlow,EYhigh)) in enumerate(zip(points,errors)):
            ret.SetPoint(i, x, y)
            ret.SetPointError(i, EXlow,EXhigh,EYlow,EYhigh)
            print("e",y,EYlow,EYhigh)
       
      ret.SetFillStyle(3244);
      ret.SetFillColor(r.kOrange+1)
      ret.SetMarkerStyle(0)
      ret.Draw("PE2 SAME")
      return ret

#CREATE Graphs and Histos to plot
if not os.path.isfile(GenInfo+"_2016.root"):
       raise RuntimeError("FATAL: file {f} does not exist. Missing Cards with Gen Info".format(f = GenInfo+"_2016.root"))
tf=r.TFile.Open(GenInfo+"_2016.root")
tf1=r.TFile.Open(GenInfo+"_2016APV.root")
tf2=r.TFile.Open(GenInfo+"_2017.root")
tf3=r.TFile.Open(GenInfo+"_2018.root")
reference = Get_Genhisto(tf,tf1,tf2,tf3,"x_TTW_inclusive") #Get MC Histogram

maxim = 0
maxY = 0

gr=r.TGraphAsymmErrors(len(reference))
grst=r.TGraphAsymmErrors(len(reference))
unc = r.TGraphAsymmErrors(len(reference))

results = {}
results_st = {}
count =0
print("g")
numbbins = reference.GetNbinsX()
print(reference.GetNbinsX(),fitResult.floatParsFinal())
#print("hey:",fitResult_stat.floatParsFinal().Print())
#print("hey:",fitResult.floatParsFinal().Print())
for v in fitResult.floatParsFinal():
        if "r_TTW" in v.GetName():
            count += 1
            print(v.GetName(), count)
            results[v.GetName()] = [ v.getVal(), abs(v.getErrorLo()), v.getErrorHi(), v.getError() ]
            if count == reference.GetNbinsX(): break
count2 =0


for v in fitResult_stat.floatParsFinal():
        if "r_TTW" in v.GetName():
            count2 += 1
            print(v.GetName())
            results_st[v.GetName()] = [ v.getVal(), abs(v.getErrorLo()), v.getErrorHi(), v.getError() ]
            if count2 == reference.GetNbinsX(): break

print("bins")
print(results)
print(results_st)
pois_0 = results.keys()


#order pois by bin number
index = []
for p in pois_0:
     i = re.sub(r'\D', "", p) #remove all items which are not numbers
     index.append(int(i))

pois = [p for _,p in sorted(zip(index,pois_0))]
print(pois)

for bin in range(reference.GetNbinsX()):
    #values=results[poiname%(bin+1)]
    values=results[pois[bin]]
    values_st=results_st[pois[bin]]
    upvar=values[2]
    dnvar=values[1]
    upvar_st=values_st[2]
    dnvar_st=values_st[1]
    nom=values[0]
    print(nom, upvar, dnvar)
    xval=reference.GetBinCenter(bin+1)
    binwidth=reference.GetBinWidth(bin+1)
    gr.SetPoint(bin, xval, nom*reference.GetBinContent(bin+1)/lumi)
    unc.SetPoint(bin, xval, reference.GetBinContent(bin+1)/lumi)
    unc.SetPointEYhigh( bin,reference.GetBinError(bin+1)/lumi)
    unc.SetPointEYlow( bin, reference.GetBinError(bin+1)/lumi)
    
    #gr.SetPointEXhigh( bin,binwidth/2)
    #gr.SetPointEXlow( bin,binwidth/2)
    gr.SetPointEYhigh( bin,(upvar)*reference.GetBinContent(bin+1)/lumi)
    gr.SetPointEYlow( bin,(dnvar)*reference.GetBinContent(bin+1)/lumi)
    grst.SetPoint(bin, xval, nom*reference.GetBinContent(bin+1)/lumi)
    #grst.SetPointEXhigh( bin,binwidth/2)
    #grst.SetPointEXlow( bin,binwidth/2)
    grst.SetPointEYhigh( bin,(upvar_st)*reference.GetBinContent(bin+1)/lumi)
    grst.SetPointEYlow( bin,(dnvar_st)*reference.GetBinContent(bin+1)/lumi)
    maxim=xval+binwidth/2
    minX = reference.GetBinCenter(1)-binwidth/2
    maxY  = max(maxY,  nom*reference.GetBinContent(bin+1)/lumi+(upvar)*reference.GetBinContent(bin+1)/lumi+reference.GetBinContent(bin+1)/lumi)*1.1


ratio = gr.Clone()
for i in xrange(ratio.GetN()):
    x    = ratio.GetX()[i]
    div  = reference.GetBinContent(reference.GetXaxis().FindBin(x))/lumi
    ratio.SetPoint(i, x, ratio.GetY()[i]/div if div > 0 else 0)
    ratio.SetPointError(i, ratio.GetErrorXlow(i), ratio.GetErrorXhigh(i), 
                  ratio.GetErrorYlow(i)/div  if div > 0 else 0, 
                  ratio.GetErrorYhigh(i)/div if div > 0 else 0) 

        
tokeep=[]
topSpamSize=1.2
plotformat = (600,600)
height = plotformat[1]+150
c1 = r.TCanvas("_canvas", '', plotformat[0], height)
p1 = r.TPad("pad1","pad1",0,0.30,1,1);
p1.SetTopMargin(p1.GetTopMargin()*topSpamSize);
p1.SetBottomMargin(0)
p1.Draw();
p2 = r.TPad("pad2","pad2",0,0,1,0.30);
p2.SetTopMargin(0)
p2.SetBottomMargin(0.3);
p2.SetFillStyle(0);
p2.Draw();
p1.cd();

t = doSpam('#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}',  0.16, .955,0.6, .995, align=12, textSize=0.033*1.4)
t1 = doSpam('138 fb^{-1} (13 TeV)',  0.67, .955,0.99, .995, align=12, textSize=0.033*1.4)



frame=r.TH1F("frame","",1, minX, maxim)
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
print("#frac{d#sigma}{d %s}"%varname[var])
frame.GetYaxis().SetTitle("#frac{d#sigma}{d %s}"%varname[var])
frame.GetXaxis().SetNdivisions(510)
frame.GetYaxis().SetRangeUser(0,maxY)
lowedge = reference.GetBinLowEdge(1)
upperedge =reference.GetBinLowEdge(numbbins+1)
frame.GetXaxis().SetRangeUser(lowedge,upperedge)

frame.Draw()

referencen = reference.Clone()
referencen.SetLineColor(r.kOrange+1);
referencen.SetLineWidth(3)
referencen.Scale(1./lumi)
reference.GetXaxis().SetRangeUser(lowedge,upperedge)
referencen.Draw("Hsame")

herrlistup = [Get_Genhisto(tf,tf1,tf2,tf3,"x_TTW_inclusive_CMS_ttWl_thu_shape_ttWUp"),Get_Genhisto(tf,tf1,tf2,tf3,"x_TTW_inclusive_QCDpdf_ttW_ACCEPTUp"),Get_Genhisto(tf,tf1,tf2,tf3,"x_TTW_inclusive_FSRUp"),Get_Genhisto(tf,tf1,tf2,tf3,"x_TTW_inclusive_ISR_ttWUp")]
herrlistdn = [Get_Genhisto(tf,tf1,tf2,tf3,"x_TTW_inclusive_CMS_ttWl_thu_shape_ttWDown"),Get_Genhisto(tf,tf1,tf2,tf3,"x_TTW_inclusive_QCDpdf_ttW_ACCEPTDown"),Get_Genhisto(tf,tf1,tf2,tf3,"x_TTW_inclusive_FSRDown"),Get_Genhisto(tf,tf1,tf2,tf3,"x_TTW_inclusive_ISR_ttWDown")]



totalError = doShadedUncertainty(reference,herrlistup,herrlistdn,lumi)  
totalError.Draw("PE2 SAME")
gr.SetLineWidth(3)
gr.Draw("PE,same")

grst.SetLineWidth(3)
grst.SetLineColor(r.kAzure-2)
grst.Draw("PE,same")

t.Draw()
t1.Draw()

entries = [[gr,"Data","lep"],[referencen,"ttW Gen","l"]]
leg=doLegend(entries)


leg.Draw()

p2.cd();
frameratio=r.TH1F("ratioframe","",1, minX, maxim)
frameratio.GetXaxis().SetTitle(varname[var])
frameratio.SetBinError(1,0)
frameratio.SetBinContent(1,1)
frameratio.GetXaxis().SetTitleFont(42)
frameratio.GetXaxis().SetTitleSize(0.14)
frameratio.GetXaxis().SetTitleOffset(0.98)
frameratio.GetXaxis().SetLabelFont(42)
frameratio.GetXaxis().SetLabelSize(0.14)
frameratio.GetXaxis().SetLabelOffset(0.015)
frameratio.GetYaxis().SetNdivisions(505)
frameratio.GetYaxis().SetTitleFont(42)
frameratio.GetYaxis().SetTitleSize(0.14)
offset = 0.62
frameratio.GetYaxis().SetTitleOffset(offset)
frameratio.GetYaxis().SetLabelFont(42)
frameratio.GetYaxis().SetLabelSize(0.14)
frameratio.GetYaxis().SetLabelOffset(0.01)
frameratio.GetYaxis().SetDecimals(True) 
frameratio.GetYaxis().SetTitle("Data/MC")
frame.GetXaxis().SetLabelOffset(999) ## send them away
frame.GetXaxis().SetTitleOffset(999) ## in outer space
frame.GetYaxis().SetTitleSize(0.06)
frame.GetYaxis().SetTitleOffset(1.2)
frame.GetYaxis().SetLabelSize(0.05)
frame.GetYaxis().SetLabelOffset(0.007)



p2.cd()
frameratio.GetXaxis().SetRangeUser(lowedge,upperedge)
frameratio.Draw()

ratio.SetLineWidth(3)
ratio.Draw("p,E,same")

c1.Update()
#gr_ratio.Draw('p,E,same')


plot=var
c1.SaveAs(folder+'/plot_noasimov_%s.png'%(plot.replace('.','p')))
c1.SaveAs(folder+'/plot_noasimov_%s.pdf'%(plot.replace('.','p')))
    
                            
