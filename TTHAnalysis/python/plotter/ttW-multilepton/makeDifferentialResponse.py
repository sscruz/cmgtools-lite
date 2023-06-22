import ROOT as r 
import re
import collections
import math 
import os,sys
from array import array
folder = sys.argv[1]
GenInfo=folder+"/"+sys.argv[2]
RecoInfo=folder+"/"+sys.argv[3]
var = sys.argv[4]
Fit=folder+"/fitDiagnosticsnominal.root"
fit_st = folder+"/fitDiagnosticsfreezing.root"

lumi =200.68 #use the lumi used to normalized the gen histos (fb-1)
varname = {"lep1_pt":("p_{T} (lep1)"),"lep1_eta":("#eta (lep1)"),"njets":("N Jet"),"nbjets":("N b-tag"),"jet1_pt":("p_{T} (jet)"),"deta_llss":("#Delta #eta (ll)"),"HT":("HT"),"dR_ll":("#Delta R (ll)"),"max_eta":("max(#eta) (ll)")}

r.gROOT.ProcessLine(".x tdrstyle.cc")
r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)
r.gROOT.SetBatch(True)
r.gStyle.SetPaintTextFormat("4.3f");
_noDelete={}
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


def doShadedUncertainty(h,lumi,relative = False):
      xaxis = h.GetXaxis()
      points = []; errors = []
      for i in xrange(h.GetNbinsX()):
            N = h.GetBinContent(i+1)/lumi;
            dN = h.GetBinError(i+1)/lumi 
            if N == 0 and (dN == 0 or relative): continue
            x = xaxis.GetBinCenter(i+1);
            EYlow = dN
            EYhigh =dN
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
      
       
      ret.SetFillStyle(3244);
      ret.SetFillColor(r.kOrange+1)
      ret.SetMarkerStyle(0)
      ret.Draw("PE2 SAME")
      return ret

tf=r.TFile.Open(str(GenInfo))
reference=tf.Get("x_TTW_inclusive")



tf_fit = r.TFile.Open(str(Fit))


maxim = 0
maxY = 0
results = {}
results_st = {}
count = 0
fitResult = tf_fit.Get('fit_s')

for v in fitResult.floatParsFinal():
        if "r_TTW" in v.GetName():
            count += 1
            results[v.GetName()] = [ v.getVal(), abs(v.getErrorLo()), v.getErrorHi(), v.getError() ]
            if count == reference.GetNbinsX(): break

pois_0 = results.keys()


tf_reco=r.TFile.Open(str(RecoInfo))
print(pois_0[0].replace("r","x"))
reference_reco=tf_reco.Get(pois_0[0].replace("r","x"))

#order pois by bin number
index = []
for p in pois_0:
     i = re.sub(r'\D', "", p) #remove all items which are not numbers
     index.append(int(i))

particle_bins = [p.replace("r_","") for _,p in sorted(zip(index,pois_0))]
print(particle_bins)


ndetectorbins = reference_reco.GetNbinsX()
nparticlebins = len(particle_bins)

detectorbins = array("d",[ reference_reco.GetXaxis().GetBinLowEdge(i) for i in range(1,ndetectorbins+2) ])
print(detectorbins)
particlebins = array("d",[ reference.GetXaxis().GetBinLowEdge(i) for i in range(1,nparticlebins+2) ])
print(particlebins)

reco_particle = r.TH2D("2dimh","2dimh",nparticlebins, particlebins, ndetectorbins, detectorbins)
hGen = r.TH2D("gen","gen",nparticlebins, particlebins, ndetectorbins, detectorbins)
particleindex = 0
for bin in particle_bins:
    particleindex +=1 
    #years:
    h1 = tf_fit.Get('shapes_fit_s/ch1/%s'%bin)
    h2 = tf_fit.Get('shapes_fit_s/ch2/%s'%bin) 
    h3 = tf_fit.Get('shapes_fit_s/ch3/%s'%bin)
    h4 = tf_fit.Get('shapes_fit_s/ch4/%s'%bin)
    h1.Add(h2)
    h1.Add(h3)
    h1.Add(h4)
    for i in range(1,ndetectorbins+1):
        reco_particle.SetBinContent(particleindex,i,h1.GetBinContent(i)/138.)

for i in range(0, nparticlebins + 2):
    for j in range(0, ndetectorbins + 2):
          hGen.SetBinContent(i, j, reference.GetBinContent(i))
          hGen.SetBinError(i, j, reference.GetBinError(i))


reco_particle.Divide(hGen)



tokeep=[]
topSpamSize=1.2
plotformat = (800,600)
#height = plotformat[1]+150
c1 = r.TCanvas("_canvas", '', plotformat[0], plotformat[1])
p1 = r.TPad("pad1","pad1",0.01,0.05,0.98,0.98);
p1.SetTopMargin(p1.GetTopMargin()*topSpamSize);
p1.SetRightMargin(0.14)
p1.Draw();
p1.cd();

t = doSpam('#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}',  0.16, .955,0.6, .995, align=12, textSize=0.033*1.4)
t1 = doSpam('138 fb^{-1} (13 TeV)',  0.67, .955,0.99, .995, align=12, textSize=0.033*1.4)
#frame=r.TH1F("frame","",1,  plotformat[0]-2,  plotformat[1]-2)
#frame.GetXaxis().SetTitleFont(42)
#frame.GetXaxis().SetTitleSize(0.06)
#frame.GetXaxis().SetTitleOffset(0.07)
#frame.GetXaxis().SetLabelFont(42)
#frame.GetXaxis().SetLabelSize(0.06)
#frame.GetXaxis().SetLabelOffset(0.007)
#frame.GetYaxis().SetTitleFont(42)
#frame.GetYaxis().SetTitleSize(0.12)
#frame.GetYaxis().SetLabelFont(42)
#frame.GetYaxis().SetLabelSize(0.12)#
#print("#frac{d#sigma}{d %s}"%varname[var])
#frame.GetYaxis().SetTitle("#frac{d#sigma}{d %s}"%varname[var])
#frame.GetXaxis().SetNdivisions(510)


#frame.Draw()
reco_particle.GetXaxis().SetTitleSize(0.055)
reco_particle.GetXaxis().SetTitle("Detector level leading %s"%varname[var])
reco_particle.GetXaxis().SetTitleOffset(1.1)
reco_particle.GetYaxis().SetTitleSize(0.055)
reco_particle.GetYaxis().SetTitle("Particle level leading %s"%varname[var])
reco_particle.GetZaxis().SetTitle("Events ")
reco_particle.GetZaxis().SetTitleOffset(1.2)
reco_particle.GetZaxis().SetTitleOffset(0.8)
reco_particle.Draw("colztext") 
t.Draw()
t1.Draw()


plot=var
c1.SaveAs(folder+'/response_%s.png'%(plot.replace('.','p')))                 
