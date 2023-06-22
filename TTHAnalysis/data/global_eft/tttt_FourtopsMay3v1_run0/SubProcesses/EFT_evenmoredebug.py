import allmatrix2py
import math 


def invert_momenta(p):
    #fortran/C-python do not order table in the same order
    new_p = []
    for i in range(len(p[0])):  
        new_p.append([0]*len(p))
    for i, onep in enumerate(p):
        for j, x in enumerate(onep):
            new_p[j][i] = x
    return new_p

def zboost(part, pboost=[]):
    """Both momenta should be in the same frame.                                                                                                                                             
The boost perform correspond to the boost required to set pboost at                                                                                                                          
    rest (only z boost applied).                                                                                                                                                             
    """
    E = pboost[0]
    pz = pboost[3]
    #beta = pz/E                                                                                                                                                                             
    gamma = E / math.sqrt(E**2-pz**2)
    gammabeta = pz  / math.sqrt(E**2-pz**2)

    out =  [gamma * part[0] - gammabeta * part[3],
            part[1],
                part[2],
                gamma * part[3] - gammabeta * part[0]]

    if abs(out[3]) < 1e-6 * out[0]:
        out[3] = 0
    return out


def get_smatrixhel_forCard( card ):
    allmatrix2py.initialise( card )
    all_prefix = [''.join(j).strip().lower() for j in allmatrix2py.get_prefix()]
    allpdgs=allmatrix2py.get_pdg_order().tolist()


    prefix_set=set(all_prefix)
    hel_dict = {}

    for prefix in prefix_set:
        hel_dict[prefix]={}
        nhel=getattr( allmatrix2py, '%sprocess_nhel' % prefix ).nhel  
        for i,onehel in enumerate(zip(*nhel)):
            hel_dict[prefix][tuple(onehel)] = i+1



    parts = [[1841.1225499,0.0,0.0,1841.1225499],
             [537.98634419,-0.0,-0.0,-537.98634419],
             [251.35700811,-50.824651551,-165.60236972,-58.453446997],
             [882.62361265,-640.21414231,336.91516992,475.27067221],
             [322.07594522,49.172741567,-93.889384055,250.4865057],
             [923.05232816,641.8660523,-77.423416148,635.83247484],
    ]

    pboost = [ parts[0][i] + parts[1][i] for i in xrange(4)]
    com_parts=[]
    for part in parts:
        com_parts.append( zboost( part, pboost) ) 
    
    
    
    com_parts = invert_momenta(com_parts)
    pdgs = [21,21,6,-6,6,-6]
    thehel_dict=hel_dict[all_prefix[allpdgs.index(pdgs)]]
    hels=(-1,-1,-1,-1,-1,-1)
    nhel=thehel_dict[hels]
    #nhel = -1 # means sum over all helicity
    
    alphas=0.09667684
    scale2=0
    ans = allmatrix2py.smatrixhel(pdgs,com_parts,alphas,scale2,nhel)
    return ans 


print("Starting point smatrix", get_smatrixhel_forCard( 'param_card_tttt.dat'))
print("SM smatrix            ", get_smatrixhel_forCard( 'param_card_tttt_sm.dat'))
