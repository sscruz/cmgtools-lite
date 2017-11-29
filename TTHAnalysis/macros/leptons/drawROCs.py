import os
import optparse
import itertools
import numpy as np
import copy
from ROOT import *
from scipy import integrate

import gc
gc.disable()
gc.set_threshold(0)
# Command line options
usage = 'usage: %prog --input]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input',   dest='inputDir',  help='input directory',        default='/tmp/doesnotexist/',           type='string')
parser.add_option('-o', '--output',  dest='outputDir', help='output directory',       default='./',           type='string')
parser.add_option('-c', '--classifiers',     dest='classifiersList', help='Which classifier should be run (comma-separated list)', default=None, type='string')
parser.add_option('-n', '--classifierName', dest='classifierNames', help='Internal names of the classifiers in TMVA', default=None)
parser.add_option('-b', '--nbins',      dest='nbins', help='Number of bins for the ROC', default=100, type='int')
parser.add_option('-s', '--smooth',     dest='smooth', help='Draw a smoothed curve instead of a binned histogram', action='store_true')
parser.add_option('-e', '--extensions', dest='extensions', help='Write the plots in the specified format (comma-separated list)', default='png,pdf,root', type='string')
parser.add_option('-y', '--logy',       dest='logy', help='Draw y axis in logy', action='store_true')
parser.add_option('--simple', dest='simple', help='Take the ROCs directly from the ROOT histograms', action='store_true')
(opt, args) = parser.parse_args()                                                                                                                        
# check if the conversions are excluded

inputDir=opt.inputDir
outputDir=opt.outputDir
classifiers=opt.classifiersList.split(',')
classifierNames=[]
if classifierNames:
    for n in opt.classifierNames.split(','):
        classifierNames.append(n)
else:
    for n in classifiers:
        classifierNames.append('BDTG')
nbins=opt.nbins
smooth=opt.smooth
extensions=opt.extensions.split(',')
logy=opt.logy

if not os.path.isdir(outputDir):
    os.mkdir(outputDir)

for flavour in ['el_eleGP', 'mu']:
    thelist=[]
    for classifier, cn in zip(classifiers, classifierNames):
        name='%s_%s' % (classifier, flavour)
        
        fname='%s/%s.root' % (inputDir, name)
        print('Processing file %s' % fname)
        
        f = TFile.Open(fname)

        bdtsig = TH1F("bdtsig", "bdt signal"    , nbins, -1., 1.)
        bdtbkg = TH1F("bdtbkg", "bdt background", nbins, -1., 1.)
        f.TestTree.Draw('%s>>bdtsig' % cn,'weight*(classID==0)')
        f.TestTree.Draw('%s>>bdtbkg' % cn,'weight*(classID==1)')
        
        cbdtsig = TH1F("cbdtsig", "bdt signal"    , nbins, -1., 1.)
        cbdtbkg = TH1F("cbdtbkg", "bdt background", nbins, -1., 1.)
      
        cbdtsig=bdtsig.GetCumulative()
        cbdtsig.Scale(1/cbdtsig.GetMaximum())
        cbdtbkg=bdtbkg.GetCumulative()
        cbdtbkg.Scale(1/cbdtbkg.GetMaximum())

        bdtx=np.zeros(nbins)
        bdty=np.zeros(nbins)
          
        for jEntry in range(1,nbins):
            bdtx[jEntry-1]=1-cbdtsig.GetBinContent(jEntry)
            bdty[jEntry-1]=cbdtbkg.GetBinContent(jEntry)

        bdtroc=bdty[0]*(bdtx[1]+bdtx[0])/2
        for jEntry in range (1,nbins-1):
            bdtroc = bdtroc + bdty[jEntry]*(bdtx[jEntry+1]-bdtx[jEntry-1])/2
        bdtroc = bdtroc + bdty[nbins-1]*(1-bdtx[nbins-2])

        gbdtroc=TGraph(nbins-1, bdtx, bdty)
        fbdtroc = lambda x : gbdtroc.Eval(x)
        bdtroc = integrate.quad(fbdtroc, 0, 1)[0]
        thelist.append([copy.deepcopy(gbdtroc), bdtroc, classifier])

    c = TCanvas("c", "c", 1000, 1000)
    c.cd() 
    if logy:
        gPad.SetLogy()
    leg = TLegend(0.3,0.3,0.58,0.58)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.025)
    for idx, val in enumerate(thelist):
        graph=val[0]
        roc=val[1]
        clas=val[2]
        graph.SetTitle("ROC curves")
        graph.GetXaxis().SetTitle("Signal efficiency")
        graph.GetYaxis().SetTitle("1-(bkg efficiency)")
        graph.Draw('AL' if idx==0 else 'sameL')
        graph.SetLineColor(idx+1)
        graph.SetLineWidth(2)
        graph.SetMarkerColor(idx+1)
        leg.AddEntry(graph,'%s: %f' % (clas, roc),"l")

    leg.Draw()
    for ext in extensions:
        c.Print('%s/rocComparison_%s.%s' % (outputDir, flavour, ext))
