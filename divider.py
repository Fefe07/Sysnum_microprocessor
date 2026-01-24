################################################################################
#########################         DIVIDER           ############################
################################################################################


from lib_carotte import *
from typing import *

from arith_unit import adder, arith_unit
from log_unit import clone, b_or


def unsigned_divider_aux(a, b):
    m = b.bus_size
    n = a.bus_size
    assert 2*m >= 2*n > m 
     
    sub, geu = arith_unit(a, b[:n], Constant("1"))
    if m == n :
        return geu, Mux(geu, a , sub)

    subtract_b = geu & ~b_or(b[n:])
    rem = Mux(subtract_b , a, sub)
    div_l, mod_l = unsigned_divider_aux(rem, b[1:])
    return div_l+subtract_b, mod_l

def unsigned_divider(a, b):
    n = a.bus_size
    return unsigned_divider_aux(a, Constant((n-1)*"0") + b)

def main() :
    n = 8
    a = Input(n)
    b = Input(n)
    div, rem = unsigned_divider(a, b)
    div.set_as_output("div")
    rem.set_as_output("remainder")

