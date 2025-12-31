################################################################################
######################       MULTIPLEXER          ##############################
################################################################################

from lib_carotte import *
from typing import *

from log_unit import clone, concat
from demux import demux

def bit_mux(sel, a) :
    assert sel.bus_size == 1
    assert a.bus_size % 2 == 0
    mid = a.bus_size//2 
    return Mux(sel, a[:mid], a[mid:])

def mux(sel, a):
    if sel.bus_size == 1 :
        return bit_mux(sel, a)
    return mux(sel[1:], bit_mux(sel[0], a))

def main():
    sel = Input(3)
    a = Input(32)

    mux(sel, a).set_as_output("r") 
    mux(sel, concat(demux(sel, a))).set_as_output("id") # devrait donner la même chose que "a"
    concat(demux(sel, mux(sel, a))).set_as_output("p")  # devrait juste mettre les bits non sélectionnées à 0 

# Exemple :
# Step 1 :
# sel ? 3
# a ? 0b11100100
# => r = 3 (0b11)
# => id = 228 (0b11100100)
# => p = 192 (0b11000000)