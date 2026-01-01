################################################################################
######################      DEMULTIPLEXER       ################################
################################################################################

from lib_carotte import *
from typing import *

from log_unit import clone

def bit_demux(sel, inp):
    ''' 1-bit demultiplexer '''
    assert sel.bus_size == 1
    allow_ribbon_logic_operations(True)
    
    n = inp.bus_size
    return [ clone(n,~sel) & inp ] + [ clone(n,sel) & inp ] 
    

def demux(sel, inp):
    ''' n-bit demultiplexer '''
    n = sel.bus_size
    if n == 1 :
        return bit_demux(sel, inp)
    first_res = bit_demux(sel[0], inp)
    branch0 = first_res[0]
    branch1 = first_res[1]
    rest_sel = sel[1:]
    return demux(rest_sel, branch0) + demux(rest_sel, branch1)

def main() :
    sel = Input(3)
    inp = Input(3)
    l = demux(sel, inp)
    for i in range(len(l)):
        l[i].set_as_output("r_"+str(i))

# Exemple
# Step 1 :
# sel ? 5
# inp ? 0b101
# => r_0 = 0 (0b000)
# => r_1 = 0 (0b000)
# => r_2 = 0 (0b000)
# => r_3 = 0 (0b000)
# => r_4 = 0 (0b000)
# => r_5 = 5 (0b101)
# => r_6 = 0 (0b000)
# => r_7 = 0 (0b000)