import ROOT as r 
import re
import collections
import math 
import os,sys
from array import array
import numpy as np
from copy import deepcopy 

#Inputs: folder region(2lss 3l) variable
folder = sys.argv[1]
region = sys.argv[2]
var = sys.argv[3]

outfolder = folder
if len(sys.argv) == 5:
   outfolder = sys.argv[4]
   os.system("mkdir -p %s"%outfolder)

lumi = 16.8+19.5+41.4+59.7#use the lumi used to normalized the gen histos (fb-1)
varname = {"lep1_pt":("p_{T} (lep1)"),"lep2_pt":("p_{T} (lep2)"),"lep1_eta":("#eta (lep1)"),"njets":("N Jet"),"nbjets":("N b-tag"),"jet1_pt":("p_{T} (jet)"),"deta_llss":("#Delta #eta (ll)"),"HT":("HT"),"dR_ll":("#Delta R (ll)"),"max_eta":("max(#eta) (ll)"), "pt3l": ("p_{T} 3l"), "m3l":("m_{3l}"),"dR_lbmedium":(" #Delta R (l bmedium)"),"mindr_lep1_jet25":("min #Delta R (lj)"),"dR_lbloose":(" #Delta R (l bloose)")}

if var not in varname.keys():
   print("Variable not included, please add")

if "2lss" in region:
   region = "2lss"
   regioncard = "2lss_0tau"
   
elif "3l" in region:
   region = "3l"
   regioncard  = "3l_0tau"
GenInfo=folder+"/ttW_"+regioncard+"_Gen_"+var


RecoInfo=folder+"/ttW_"+regioncard+"_"+var 

#Get info needed from the fit
Fit = folder+"/fitDiagnosticsnominal_"+var+"_"+region+".root"
fit_st = folder+"/fitDiagnosticsfreezing_"+var+"_"+region+".root"
ws = folder+"/ws_"+var+"_"+region+".root"

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


def combineyears(tf,tf1,tf2,tf3,name):
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

def combineyears_andchannels(tf,tf1,tf2,tf3,tf4,tf5,tf6,tf7,name):
    print(name)
    reference1=tf.Get(name)
    reference2=tf1.Get(name)
    reference3=tf2.Get(name)
    reference4=tf3.Get(name)
    reference5=tf4.Get(name)
    reference6=tf5.Get(name)
    reference7=tf6.Get(name)
    reference8=tf7.Get(name)
    reference = reference1.Clone("reference"+name)
   
    reference.Add(reference2)
    reference.Add(reference3)
    reference.Add(reference4)
    reference.Add(reference5)
    reference.Add(reference6)
    reference.Add(reference7)
    reference.Add(reference8)
    
    return reference

#CREATE Graphs and Histos to plot
if not os.path.isfile(GenInfo+"_2016.root"):
       raise RuntimeError("FATAL: file {f} does not exist. Missing Cards with Gen Info".format(f = GenInfo+"_2016.root"))
tf=r.TFile.Open(GenInfo+"_2016.root")
tf1=r.TFile.Open(GenInfo+"_2016APV.root")
tf2=r.TFile.Open(GenInfo+"_2017.root")
tf3=r.TFile.Open(GenInfo+"_2018.root")

reference = combineyears(tf,tf1,tf2,tf3,"x_TTW_inclusive") #Get MC Histogram



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


#CREATE Reco Graphs and Histos to plot
if "3l" in region:
   if not os.path.isfile(RecoInfo+"_2016.root"):
       raise RuntimeError("FATAL: file {f} does not exist. Missing Cards with Reco Info".format(f = RecoInfo+"_2016.root"))

   tfr=r.TFile.Open(RecoInfo+"_2016.root")
   tf1r=r.TFile.Open(RecoInfo+"_2016APV.root")
   tf2r=r.TFile.Open(RecoInfo+"_2017.root")
   tf3r=r.TFile.Open(RecoInfo+"_2018.root")

   reference_reco = combineyears(tfr,tf1r,tf2r,tf3r,pois_0[0].replace("r_TTW","x_TTW")) #Get reco Histogram


elif "2lss" in region:
   if not os.path.isfile(RecoInfo+"_2016_negative.root"):
       raise RuntimeError("FATAL: file {f} does not exist. Missing Cards with Reco Info".format(f = RecoInfo+"_2016_negative.root"))

   tfr=r.TFile.Open(RecoInfo+"_2016_negative.root")
   tf1r=r.TFile.Open(RecoInfo+"_2016APV_negative.root")
   tf2r=r.TFile.Open(RecoInfo+"_2017_negative.root")
   tf3r=r.TFile.Open(RecoInfo+"_2018_negative.root")
   tf4r=r.TFile.Open(RecoInfo+"_2016_positive.root")
   tf5r=r.TFile.Open(RecoInfo+"_2016APV_positive.root")
   tf6r=r.TFile.Open(RecoInfo+"_2017_positive.root")
   tf7r=r.TFile.Open(RecoInfo+"_2018_positive.root")

   reference_reco = combineyears_andchannels(tfr,tf1r,tf2r,tf3r,tf4r,tf5r,tf6r,tf7r,pois_0[0].replace("r_TTW","x_TTW")) #Get reco Histogram

#order pois by bin number
index = []
for p in pois_0:
     i = re.sub(r'\D', "", p) #remove all items which are not numbers
     index.append(int(i))

particle_bins = [p.replace("r_TTW","TTW") for _,p in sorted(zip(index,pois_0))]
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
    if "3l" in region:
       h1 = tf_fit.Get('shapes_fit_s/ch1/%s'%bin)
       h2 = tf_fit.Get('shapes_fit_s/ch2/%s'%bin) 
       h3 = tf_fit.Get('shapes_fit_s/ch3/%s'%bin)
       h4 = tf_fit.Get('shapes_fit_s/ch4/%s'%bin)
       h1.Add(h2)
       h1.Add(h3)
       h1.Add(h4)
    elif "2lss" in region:
       h1 = tf_fit.Get('shapes_fit_s/ch1/%s'%bin)
       h2 = tf_fit.Get('shapes_fit_s/ch2/%s'%bin) 
       h3 = tf_fit.Get('shapes_fit_s/ch3/%s'%bin)
       h4 = tf_fit.Get('shapes_fit_s/ch4/%s'%bin)
       h5 = tf_fit.Get('shapes_fit_s/ch5/%s'%bin)
       h6 = tf_fit.Get('shapes_fit_s/ch6/%s'%bin) 
       h7 = tf_fit.Get('shapes_fit_s/ch7/%s'%bin)
       h8 = tf_fit.Get('shapes_fit_s/ch8/%s'%bin)
       h1.Add(h2)
       h1.Add(h3)
       h1.Add(h4)
       h1.Add(h5)
       h1.Add(h6)
       h1.Add(h7)
       h1.Add(h8)
    for i in range(1,ndetectorbins+1):
        reco_particle.SetBinContent(particleindex,i,h1.GetBinContent(i)/lumi)

for i in range(0, nparticlebins + 2):
    for j in range(0, ndetectorbins + 2):
          hGen.SetBinContent(i, j, reference.GetBinContent(i)/lumi)
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
reco_particle.GetYaxis().SetTitle("Detector level %s"%varname[var])
reco_particle.GetXaxis().SetTitleOffset(1.1)
reco_particle.GetYaxis().SetTitleSize(0.055)
reco_particle.GetXaxis().SetTitle("Particle level %s"%varname[var])
reco_particle.GetZaxis().SetTitle("Events ")
reco_particle.GetZaxis().SetTitleOffset(1.2)
reco_particle.GetZaxis().SetTitleOffset(0.8)
reco_particle.Draw("colztext") 
t.Draw()
t1.Draw()


plot=var
c1.SaveAs(outfolder+'/response_%s_%s.png'%(plot.replace('.','p'),region))                 
## Compute purity and stability with the response matrix
# X: detector level
# Y: particle level

def compute_purity(hist, reference):
    """ 
    Sum over particle level for a given detector level bin 
    """
    
    nBinsX = hist.GetNbinsX()
    nBinsY = hist.GetNbinsY()
    isSquare = (nBinsX == nBinsY)

    purity_h = deepcopy(reference.Clone("purity_h")) 
    if not isSquare:
       sign = 1 
       for j in range(1, nBinsY + 1, 2):
           particle_index = int(np.floor( (j+1)/2 ))
           num = hist.GetBinContent(particle_index, j) + hist.GetBinContent(particle_index, j+1)
           denom = sum([ hist.GetBinContent(i, j) for i in range(1, 1+nBinsX)])
           denom += sum([ hist.GetBinContent(i, j+1) for i in range(1, 1+nBinsX)])

           #print("    + Num: M(%d, %d)"%(particle_index, j))
           #print("    + den: sum_i[ M(i, %d) + M(i, %d)]"%(j, j+sign))
           
           pj = num / denom if denom else 0
           sign *= -1
           #print("    + Purity in bin %d: %3.2f"%(j, pj))
           #print(" ------ ")
           purity_h.SetBinContent(particle_index, pj)
    else:
       for j in range(1, nBinsY + 1):
           num = hist.GetBinContent(j, j)
           denom = sum([ hist.GetBinContent(i, j) for i in range(1, 1+nBinsX)])


           #print("    + Num: M(%d, %d)"%(particle_index, j))
           #print("    + den: sum_i[ M(i, %d) + M(i, %d)]"%(j, j+sign))
           
           pj = num / denom if denom else 0
           #print("    + Purity in bin %d: %3.2f"%(j, pj))
           #print(" ------ ")
           purity_h.SetBinContent(j, pj)
          
    return purity_h

def compute_stability(hist, reference):
    """ 
    Sum over particle level for a given detector level bin 
    """

    nBinsX = hist.GetNbinsX()
    nBinsY = hist.GetNbinsY()

    isSquare = (nBinsX == nBinsY)

    stability_h = deepcopy(reference.Clone("stability_h")) 
   
    if not isSquare: 
        sign = 1
        for i in range(1, nBinsX + 1):
            reco_index = 2*i-1 
            num = hist.GetBinContent(i, reco_index) + hist.GetBinContent(i, reco_index+1) 
            denom = sum([ hist.GetBinContent(i, j) for j in range(1, 1+nBinsY)])
            s = num / denom if denom else 0
            #print("    + Num: M(%d, %d) + M(%d, %d)"%(i, reco_index, i, reco_index+1))
            #print("    + den: sum_j[M(%d, j)]"%(i))
            #print("    + Stability in bin %d: %3.2f"%(j+1, s))
            #print(" ------ ")
            sign *= -1
            stability_h.SetBinContent(i, s)
    else:
        for i in range(1, nBinsX + 1):
            num = hist.GetBinContent(i, i)
            denom = sum([ hist.GetBinContent(i, j) for j in range(1, 1+nBinsY)])
            s = num / denom if denom else 0
            #print("    + Num: M(%d, %d) + M(%d, %d)"%(i, reco_index, i, reco_index+1))
            #print("    + den: sum_j[M(%d, j)]"%(i))
            #print("    + Stability in bin %d: %3.2f"%(j+1, s))
            #print(" ------ ")
            stability_h.SetBinContent(i, s)
    
    return stability_h

purity_histo    = compute_purity(reco_particle, reference)
stability_histo = compute_stability(reco_particle, reference)

# Add some cosmetics
purity_histo.SetLineColor(r.kRed)
purity_histo.SetLineWidth(2)

stability_histo.SetLineColor(r.kBlue)
stability_histo.SetLineWidth(2)
stability_histo.GetYaxis().SetRangeUser(0, 1.1)
stability_histo.GetXaxis().SetTitle(varname[var])



t2 = doSpam('138 fb^{-1} (13 TeV)',  0.52, .955, 0.89, .995, align=12, textSize=0.033*1.4)

l = r.TLegend(0.55, 0.75, 0.65, 0.85)
l.SetBorderSize(0)
l.SetTextSize(0.04)
l.SetFillColor(0)
l.SetShadowColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)

l.AddEntry(purity_histo, "Purity", "l")
l.AddEntry(stability_histo, "Stability", "l")

c1 = r.TCanvas("_canvas_ps", '', 600, 750)
p1 = r.TPad("pad1","pad1",0.01,0.05,0.98,0.98)
p1.SetTopMargin(p1.GetTopMargin()*topSpamSize)
p1.SetRightMargin(0.14)
p1.Draw()
p1.cd()

# Reduce label size for HT 
if var == "HT": 
    #stability_histo.GetXaxis().SetLabelSize(0.03)
    stability_histo.GetXaxis().SetNdivisions(-4)
stability_histo.Draw("hist")

purity_histo.Draw("hist same")
t.Draw("same")
t2.Draw("same")
l.Draw("same")

c1.SaveAs(outfolder+'/purityAndStability_%s.png'%(plot.replace('.','p')))
c1.SaveAs(outfolder+'/purityAndStability_%s.pdf'%(plot.replace('.','p')))

# Write a log with the values
f = open(outfolder+"/purityAndStability_%s.txt"%(plot.replace('.', 'p')), "w")
for bini in range(1, 1+purity_histo.GetNbinsX()):
    f.write("+ Bin: %d, purity=%3.2f, stability=%3.2f\n"%(bini, purity_histo.GetBinContent(bini), stability_histo.GetBinContent(bini)))
f.close()
