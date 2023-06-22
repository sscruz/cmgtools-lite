
all_WCs=['cQlMi', 'ctq8', 'ctli', 'cpQM', 'cQq81', 'cQl3i', 'ctlTi', 'cQei', 'ctG', 'ctp', 'cptb', 'cQq13', 'ctZ', 'ctW', 'ctei', 'cpQ3', 'cbW', 'ctt1', 'cQq83', 'cQq11', 'cQQ1', 'cpt', 'ctlSi', 'cQt1', 'cQt8', 'ctq1']

dictList = dict([
    ('ctp'   , ['ctp']),
    ('cpQM'  , ['cpQM']),
    ('cpQ3'  , ['cpQ3']),
    ('cpt'   , ['cpt']), 
    ('cptb'  , ['cptb']),
    ('ctW'   , ['ctW']), 
    ('ctZ'   , ['ctZ']), 
    ('cbW'   , ['cbW']), 
    ('ctG'   , ['ctG']), 
    ('cQei'  , ['cQe1','cQe2','cQe3']),
    ('ctli'  , ['ctl1','ctl2','ctl3']),
    ('ctei'  , ['cte1','cte2','cte3']),
    ('cQl3i' , ['cQl31','cQl32','cQl33']),
    ('cQlMi' , ['cQlM1','cQlM2','cQlM3']),
    ('ctlSi' , ['ctlS1','ctlS2','ctlS3']),
    ('ctlTi' , ['ctlT1','ctlT2','ctlT3']),
    ('cQQ1'   , ['cQQ1']),
    ('cQQ8'   , ['cQQ8']),
    ('cQt1'   , ['cQt1']),
    ('cQt8'   , ['cQt8']),
    ('cQb1'   , ['cQb1']),
    ('cQb8'   , ['cQb8']),
    ('ctt1'   , ['ctt1']),
    ('ctb1'   , ['ctb1']),
    ('cQtQb1' , ['cQtQb1']),
    ('cQtQb8' , ['cQtQb8']),
    ('cQq13' , ['cQq13']),
    ('cQq83' , ['cQq83']),
    ('cQq11' , ['cQq11']),
    ('cQq81' , ['cQq81']),
    ('cQu1'  , ['cQu1']),
    ('cQu8'  , ['cQu8']),
    ('cQd1'  , ['cQd1']),
    ('cQd8'  , ['cQd8']),
    ('ctq1'  , ['ctq1']),
    ('ctq8'  , ['ctq8']),
    ('ctu1'  , ['ctu1']),
    ('ctu8'  , ['ctu8']),
    ('ctd1'  , ['ctd1']),
    ('ctd8'  , ['ctd8'])
])

process_dict = {
    'tHq' : "tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
    'tllq' : "tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
    'ttH' : "ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
    'ttll' : "ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
    'ttln' : "ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
    'tttt' : "tttt_FourtopsMay3v1_run0",
}

for key,proc in process_dict.iteritems():
    sm_card=open("%s/Cards/param_card.dat"%proc).read()
    for op in all_WCs:
        for subop in dictList[op]:
                new_card=sm_card.replace("0.000000e+00 # %s \n"%subop, "{%s} # %s\n"%(op,subop))
                if new_card == sm_card:
                      raise RuntimeError("We could not replace", subop)
                sm_card=new_card
    outf=open("param_card_template_%s.dat"%key,'w')
    outf.write( sm_card ) 
    outf.close()

    
