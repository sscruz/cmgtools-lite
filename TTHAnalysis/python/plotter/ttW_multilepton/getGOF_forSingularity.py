
import os, sys, argparse, math, json
from differential_variables import all_vars
combinerepo = sys.argv[1] 

path = sys.argv[2] #folder to run
varName = sys.argv[3]    #diff var (is a name for files)
regName = sys.argv[4] # 3l or 2lss
jobs = 50
toys = 10 #perjob

bins_particle = eval(all_vars[(varName,regName)].CATBINS_Gen)
nparticlebins   = len(bins_particle) - 1
    
    
thepois = ",".join( ["r_TTW_%s_bin%d"%(varName,i) for i in range(nparticlebins)] )

comm = "combine -M GoodnessOfFit {incard} --algo=saturated -t {Toys}  -s {seed} -n .toy_{seed}  --setParameters {pois}  --toysFrequentist;"

submit = '''sbatch  -p batch  --wrap 'cmssw-cc7  --command-to-run "cd {combp} && cmsenv &&  cd {Path} && combine -M GoodnessOfFit {incard} --algo=saturated -t {Toys}  -s {seed} -n .toy_{seed}  --setParameters {pois}  --toysFrequentist;" ' '''

for i in range(1,jobs+1):
    torun = submit.format(combp = combinerepo, Path = os.environ['PWD']+"/"+path , incard ="ws_"+varName+"_"+regName+".root",  Toys = str(toys), seed =str(i) , pois = thepois)
    print(torun)
    os.system(torun)



