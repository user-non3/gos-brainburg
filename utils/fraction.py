from . import *

LVMC = ['LVMC', 'lvmc', 'Lvmc']
LSMC = ['LSMC', 'lsmc', 'Lsmc']

GOV = ['GOV', 'gov', 'Gov']
LC = ['LC', 'lc', 'Lc']

CNNLS = ['CNN LS', 'cnn ls', 'Cnn Ls']
CNNLV = ['CNN LV', 'cnn lv', 'Cnn Lv']

def GetFractionID(word):
    if word in GOV:
        return 'GOV'

    elif word in LSMC:
        return 'LSMC'
        
    elif word in LVMC:
        return 'LVMC'
    
    elif word in LC:
        return 'LC'
    
    elif word in CNNLS:
        return 'CNN LS'
    
    elif word in CNNLV:
        return 'CNN LV'
    
def GetFractionList(fraction):
    if fraction == 3:
        return True
    
    elif fraction == 4:
        return True

    else:
        return False