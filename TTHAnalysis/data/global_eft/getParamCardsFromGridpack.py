import tarfile
import os 

path = "/pnfs/psi.ch/cms/trivcat/store/user/sesanche/TOP_22_006_gridpacks/"
gridpacklist =  { 
    'tttt' : 'tttt_FourtopsMay3v1_run0_slc7_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
    'ttH'  : 'ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0_slc7_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
    'ttln' : 'ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0_slc7_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
    'ttll' : 'ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0_slc7_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
    'tllq' : 'tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0_slc7_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
    'tHq'  : 'tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0_slc7_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz', 
}

for process in gridpacklist:
    file=tarfile.open(path+gridpacklist[process])
    things=[]
    for mem in file.getmembers():
        if mem.name in ["process/madevent/Cards/param_card.dat","process/madevent/Cards/proc_card_mg5.dat"]: things.append(mem)
    file.extractall(members=things)
    os.system('mv process/madevent/Cards/param_card.dat param_card_%s.dat'%process)
    os.system('mv process/madevent/Cards/proc_card_mg5.dat proc_card_%s.dat'%process)

