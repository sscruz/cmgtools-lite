import ROOT as r 
import sys 
from copy import deepcopy
from collections import defaultdict
import math 
SAFE_COLOR_LIST=[
r.kRed, r.kGreen+2, r.kBlue, r.kMagenta+1, r.kOrange+7, r.kCyan+1, r.kGray+2, r.kViolet+5, r.kSpring+5, r.kAzure+1, r.kPink+7, r.kOrange+3, r.kBlue+3, r.kMagenta+3, r.kRed+2,
]+range(11,40)


r.gROOT.ProcessLine(".x tdrstyle.cc")
r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)
r.gROOT.SetBatch(True)



lumi = 16.8+19.5+41.4+59.7#use the lumi used to normalized the gen histos (fb-1)

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

varname = {"lep1_pt":("p_{T} (lep1)"),"lep2_pt":("p_{T} (lep2)"),"lep1_eta":("#eta (lep1)"),"lep2_eta":("#eta (lep2)"),"njets":("N Jet"),"njets_7bins":("N Jet"),"nbjets":("N b-tag Loose"),"jet1_pt":("p_{T} (jet)"),"jet1_eta":("|#eta| (jet1)"),"deta_llss":("#Delta #eta (ll)"),"HT":("HT"),"dR_ll":("#Delta R (ll)"),"max_eta":("max(#eta) (ll)"), "pt3l": ("p_{T} 3l"), "m3l":("m_{3l}"),"dR_lbmedium":(" #Delta R (l bmedium)"),"mindr_lep1_jet25":("min #Delta R (lj)"),"dR_lbloose":(" #Delta R (l bloose)"),"jet2_pt":(" p_{T} (jet 2)"),"jet2_eta":(" |#eta| (jet 2)"),"bLooseLeadingJet_eta":(" |#eta| (bLoose 1)"),"bLooseLeadingJet_pt":(" p_{T}  (bLoose 1)"),"bMediumLeadingJet_eta":(" |#eta| (bMedium 1)"),"bMediumLeadingJet_pt":(" p_{T}  (bMedium 1)"),"sum_2lss_pt":(" p_{T}^{lep1}+p_{T}^{lep2}  "),"nbjets_medium":(" N b-tag medium ") ,"mll":(" m_ll ")  }

var=sys.argv[1]
card_path=sys.argv[2]

gen_card="{card_path}/ttW_2lss_0tau_Gen_{var}_{year}.root"

tf=r.TFile.Open(gen_card.format(card_path=card_path, var=var, year="2016"))

template_hist=deepcopy(tf.Get("x_TTW_inclusive").Clone("template_hist"))
template_hist.Reset()
template_hist.SetFillColor(0)
template_hist.SetTitle("")

# read splitted uncertainties from txt files 
relative_uncs=defaultdict(list)
for ibin in range(template_hist.GetNbinsX()):
    results = open("{card_path}/individual/outputfit_r_TTW_{var}_bin{ibin}.txt".format(card_path=card_path, var=var,ibin=ibin))
    total=0
    for l in results.readlines():
        fields = l.rstrip().split(":")
        if len( fields) == 2: 
            central_value = eval(fields[1])
        else:
            down_rel_var = eval(fields[1]) / central_value
            up_rel_var   = eval(fields[2]) / central_value
            avg_rel_var  = (up_rel_var + down_rel_var)/2
            relative_uncs[fields[0]].append( avg_rel_var)
            total=total+avg_rel_var**2
    relative_uncs['total'].append(math.sqrt(total))
        

    
# now create histos
hists={}
for unc in relative_uncs:
    unc_hist=deepcopy(template_hist.Clone(unc))
    for ibin,content in enumerate(relative_uncs[unc]):
        unc_hist.SetBinContent(ibin+1, content)
        unc_hist.SetBinError(ibin+1, 0)
    hists[unc]=unc_hist

tokeep=[]
topSpamSize=1.2
plotformat = (600,600)
height = plotformat[1]
c1 = r.TCanvas("_canvas", '', plotformat[0], height)
c1.SetTopMargin(c1.GetTopMargin()*topSpamSize);
c1.SetBottomMargin(0.125)
c1.SetLeftMargin(0.225)
c1.Draw();

hists['total'].Draw()
hists['total'].GetXaxis().SetTitleFont(42)
hists['total'].GetXaxis().SetTitleSize(0.06)
hists['total'].GetXaxis().SetTitleOffset(0.85)
hists['total'].GetXaxis().SetLabelFont(42)
hists['total'].GetXaxis().SetLabelSize(0.06)
hists['total'].GetXaxis().SetLabelOffset(0.0)
hists['total'].GetYaxis().SetTitleFont(42)
hists['total'].GetYaxis().SetTitleSize(0.06)
hists['total'].GetYaxis().SetLabelFont(42)
hists['total'].GetYaxis().SetLabelSize(0.06)
hists['total'].GetXaxis().SetNdivisions(510)


hists['total'].GetYaxis().SetRangeUser(0,0.6)
hists['total'].GetYaxis().SetTitle("#frac{d#sigma}{d %s} relative uncertainty"%varname[var])
hists['total'].GetYaxis().SetTitleOffset(1.75)
hists['total'].GetXaxis().SetTitle(varname[var])
hists['total'].SetLineColor(r.kBlack)

leg=r.TLegend(0.275,0.63,0.925,0.925)
leg.AddEntry( hists['total'], 'Total','l')
leg.SetNColumns(2)
for i,unc in enumerate(hists):
    hists[unc].SetLineWidth(4)
    if unc != 'total':
        leg.AddEntry(hists[unc], unc.replace("inc_",""),'l')
        hists[unc].SetLineColor(SAFE_COLOR_LIST[i])
        hists[unc].SetLineStyle(9)
    hists[unc].Draw('same')
leg.Draw("same")

t = doSpam('#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}',  0.205, .955,0.6, .995, align=12, textSize=0.033*1.4)
t1 = doSpam('138 fb^{-1} (13 TeV)',  0.63, .955,0.99, .995, align=12, textSize=0.033*1.4)

c1.SaveAs('{card_path}/breakdown_{var}.png'.format(card_path=card_path,var=var))
        

    
            



