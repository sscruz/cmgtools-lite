import os
import ROOT as r
import array
import sys
r.gROOT.SetBatch(1)

def color_msg(msg, color = "none"):
    """ Prints a message with ANSI coding so it can be printout with colors """
    codes = {
        "none" : "0m",
        "green" : "1;32m",
        "red" : "1;31m",
        "blue" : "1;34m",
        "yellow" : "1;35m"
    }

    print("\033[%s%s \033[0m"%(codes[color], msg))
    return

year=sys.argv[1]
treespath="/lustrefs/hdd_pool_dir/nanoAODv9/ttH_differential/NanoTrees_UL_v2_060422_skim2lss_newfts/%s/"%year
# Define groups to measure btagging efficiencies
# Just put regexpresions that match only the samples you want in the given group
groups = {
    # v1: simplistic
    "TT_dilep" : [
        "TTto2L",
    ],
    "WZ" : [
        "WZto3L"
    ]
}

# WPs to test
WPs = ["L", "M", "T"]
flavors = {"B":"B", "C":"C", "L":"L"}
passVar = "JetPassWP{wp}FL{fl}_{var}"
failVar = "JetFailWP{wp}FL{fl}_{var}"
outdir = "./btagEffs/"

for algo in ["Deepjet"]:
    for groupname, procs in groups.items():
        out = os.path.join(outdir, algo, groupname)
        if not os.path.exists( out ):
            os.system(" mkdir -p %s"%( out ))
        color_msg(" >> Measuring b tagging effs for group: %s"%groupname, "green")
        
        # Create the chain
        tChain = r.TChain()
        
        
        # Not very efficient but who cares
        files_toAdd = []
        files = os.listdir( os.path.join(treespath, "btagEffs_{algo}".format(algo = algo)))

        for file_ in files:
            for proc in procs:
                if proc in file_: 
                    files_toAdd.append(file_)
        color_msg(" >> Considering the following processes:")
        print(files_toAdd)
        for rf in files_toAdd:
            tChain.Add( os.path.join(treespath, "btagEffs_{algo}".format(algo = algo), rf + "/Friends"))
    
    
        # Prepare output
        outfile = os.path.join( out, "btagEff_{}_{}_{}.root".format(algo, groupname, year))
        theAlgFile = r.TFile(outfile, "RECREATE")


        for wp in WPs:
            color_msg("   + WP %s"%wp, "blue")
            for f in flavors.keys():
                color_msg("     From %s"%f)
                
                subs_pt = {"wp" : wp, "fl": f, "var" : "pt_nom", "algo" : algo }
                subs_eta = {"wp" : wp, "fl": f, "var" : "eta", "algo" : algo }
                
                # Evaluate the 2D histos
                passVar_eval = "{pt}:abs({eta}) >> hPasst(25,0,2.5,200,0,1000)".format( pt = passVar.format(**subs_pt), eta = passVar.format(**subs_eta) )
                failVar_eval = "{pt}:abs({eta}) >> hFailt(25,0,2.5,200,0,1000)".format( pt = failVar.format(**subs_pt), eta = failVar.format(**subs_eta) )

                tChain.Draw(passVar_eval)
                tChain.Draw(failVar_eval)
                
                hPasst = r.gDirectory.Get("hPasst")
                hFailt = r.gDirectory.Get("hFailt")
                hPass = r.TH2F("hp_{wp}_{fl}_{var}_{algo}".format(**subs_pt),"hp", 3, array.array('d',[0, 0.8, 1.6, 2.5]), 8, array.array('d', [0, 30, 50, 70, 100, 140, 200, 300, 600, 1000]))
                hFail = r.TH2F("hf_{wp}_{fl}_{var}_{algo}".format(**subs_pt),"hf", 3, array.array('d',[0, 0.8, 1.6, 2.5]), 8, array.array('d', [0, 30, 50, 70, 100, 140, 200, 300, 600, 1000]))
        
                for i in range(1,hPasst.GetNbinsX()+1):
                    for j in range(1,hPasst.GetNbinsY()+1):
                        bidx = hPass.FindBin( hPasst.GetXaxis().GetBinCenter(i), hPasst.GetYaxis().GetBinCenter(j))
                        hPass.SetBinContent( bidx,  hPass.GetBinContent(bidx) + hPasst.GetBinContent(i,j) )
                        hFail.SetBinContent( bidx,  hFail.GetBinContent(bidx) + hFailt.GetBinContent(i,j) )
                hTotal = hFail
                hTotal.Add(hPass)

                #We need to put the non-central terms to 0 or TEfficiency crashes
                for i in range(0,hPass.GetNbinsX()+2):
                    hPass.SetBinContent(i, 0, 0)
                for i in range(0,hPass.GetNbinsY()+2):
                    hPass.SetBinContent(0, i, 0)
                
                
                # Prepare keys and plots
                name = "btagEff_%s_%s_%s"%( groupname, wp, f )
                hPass.Sumw2()
                hTotal.Sumw2()
                eTemp = r.TEfficiency(hPass, hTotal)
                eTemp.SetName(name)
                
                # Create a new TH2D histogram
                n_bins_x = eTemp.GetPassedHistogram().GetNbinsX()
                n_bins_y = eTemp.GetPassedHistogram().GetNbinsY()
                hist_2d = r.TH2D(name+"_h2d", "Efficiency as TH2D",
                                    n_bins_x, eTemp.GetPassedHistogram().GetXaxis().GetBinLowEdge(1),
                                    eTemp.GetPassedHistogram().GetXaxis().GetBinUpEdge(n_bins_x),
                                    n_bins_y, eTemp.GetPassedHistogram().GetYaxis().GetBinLowEdge(1),
                                    eTemp.GetPassedHistogram().GetYaxis().GetBinUpEdge(n_bins_y))

                # Fill the TH2D histogram with the efficiency values
                for i in range(1, n_bins_x + 1):
                    for j in range(1, n_bins_y + 1):
                        eff = eTemp.GetEfficiency(eTemp.GetPassedHistogram().GetBin(i, j))
                        hist_2d.SetBinContent(i, j, eff)

                # Set labels and titles if needed
                hist_2d.GetXaxis().SetTitle(eTemp.GetPassedHistogram().GetXaxis().GetTitle())
                hist_2d.GetYaxis().SetTitle(eTemp.GetPassedHistogram().GetYaxis().GetTitle())
                hist_2d.SetTitle(eTemp.GetTitle())

                theAlgFile.cd()
                hist_2d.Write()
                
                c = r.TCanvas("c_%s"%name,"", 800,600)
                c.SetLogy(True)
                eTemp.Draw()
                c.Update() #If we don't do this, we don't get to take the PaintedHistogram
                hTemp = eTemp.GetPaintedHistogram()
                hTemp.Sumw2(False)
                for i in range(1,hTemp.GetNbinsX()+1):
                    for j in range(1,hTemp.GetNbinsY()+1):
                        hTemp.SetBinError(i,j, max(eTemp.GetEfficiencyErrorLow(eTemp.GetGlobalBin(i,j)), eTemp.GetEfficiencyErrorUp(eTemp.GetGlobalBin(i,j))))
                        #print hTemp.GetBinContent(i,j), hTemp.GetBinError(i,j)
                hTemp.SetTitle(name)
                hTemp.GetXaxis().SetTitle("Jet #eta")
                hTemp.GetYaxis().SetTitle("Jet p_{T} [GeV]")
                r.gStyle.SetPaintTextFormat("4.3f")
                #hTemp.Sumw2(False)
                hTemp.Draw("colz text E")
                c.SaveAs("%s/%s_%s.pdf"%(out, name, year))
                c.SaveAs("%s/%s_%s.png"%(out, name, year))
                c.SaveAs("%s/%s_%s.root"%(out, name, year))
