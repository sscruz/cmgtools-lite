for file in `ls /work/sesanche/ttH/UL/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/eft/*proc*.dat`; do cat ${file} | ./bin/mg5_aMC ; done
