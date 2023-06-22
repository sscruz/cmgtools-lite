import ROOT as r 
import os,sys

folder = sys.argv[1] #folder to run
var = sys.argv[2]    #diff var (is a name for files)
todo = sys.argv[3]   #step of tehe fitting to run
print(todo)
cards = [file for file in os.listdir(folder) if ".txt" in file and "Gen" not in file]
print("Found the following Cards:")
print(cards)
    

#Read the Card and get the pois
f = open(folder+"/"+cards[0], "r")
signals = []
for l in f.readlines():
    if "process" in l:
        p = l.split(" ")
        for item in p:
            if "TTW_" in item and not "ooa" in item:
                signals.append(item)
        
if todo == "0":
   print("I'm combining them")
   os.chdir(folder)
   #Combine Cards
   c = "combineCards.py "
   for item in cards:
     c += item+" "

   c += " > combined_"+var+".dat"

   print(c)
   os.system(c)


#Run workspace
if todo == "1":
   pois = ""
   for signal in signals:
       pois += " --PO 'map=.*/%s:r_%s[1,-5,10]'"%(signal,signal)

   ws = "text2workspace.py {CARD} -o {WS_NAME} -P  HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose {POIS}".format(CARD = "combined_"+var+".dat", WS_NAME = "ws_"+var+".root",POIS = pois)
   os.chdir(folder)
   
   print(ws)
   os.system(ws)

#Run fit
if todo == "2":
   
   params = ""
   for signal in signals:
       params += "r_%s=1,"%(signal)

   rf = "combine -M FitDiagnostics {WS_NAME} -m 125  --setParameters {POIS}  --freezeParameters MH --saveWorkspace --saveShapes --saveWithUncertainties -n nominal --robustFit 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000".format(WS_NAME ="ws_"+var+".root",POIS = params )
   

   #Run fit for stat

   rff = "combine -M FitDiagnostics %s -m 125  --setParameters %s --freezeParameters MH,'rgx{lumi.*}','rgx{CMS_eff.*}','rgx{CMS_ttWl.*}','rgx{CMS_ttHl.*}','rgx{CMS_scale_j.*}',CMS_jesHEMIssue,'rgx{CMS_res_j.*}','rgx{QCDscale_.*}','rgx{pdf_.*}','rgx{BR_.*}',CMS_ttWl_UnclusteredEn  --saveWorkspace --saveShapes --saveWithUncertainties -n freezing --robustFit 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000"%("ws_"+var+".root",params )
   os.chdir(folder)
   print('sbatch -c 5 -p batch --wrap "'+rf+'"')
   print('sbatch -c 5 -p batch --wrap "'+rff+'"')
   os.system('sbatch -c 5 -p batch --wrap "'+rf+'"')
   os.system('sbatch -c 5 -p batch --wrap "'+rff+'"')
