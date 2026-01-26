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
    assert a.bus_size == b.bus_size
    n = a.bus_size
    return unsigned_divider_aux(a, Constant((n-1)*"0") + b)

def conditionnal_neg(x, negate):
    n = x.bus_size
    return arith_unit(Constant(n*"0"), x, negate)[0]

def signed_divider(a, b):
    assert a.bus_size == b.bus_size
    n = a.bus_size
    a_abs = conditionnal_neg(a, a[n-1])
    b_abs = conditionnal_neg(b, b[n-1])
    div, rem = unsigned_divider(a_abs, b_abs)
    return conditionnal_neg(div, a[n-1] ^ b[n-1]), conditionnal_neg(rem, a[n-1])

def divider(a, b, is_signed): 
    n = a.bus_size
    a_abs = conditionnal_neg(a, a[n-1] & is_signed)
    b_abs = conditionnal_neg(b, b[n-1] & is_signed)
    div, rem = unsigned_divider(a_abs, b_abs)
    return conditionnal_neg(div, (a[n-1] ^ b[n-1]) & is_signed ), conditionnal_neg(rem, a[n-1] & is_signed)

def main() :
    n = 8
    a = Input(n)
    b = Input(n)
    is_signed = Input(1)
    div, rem = divider(a, b, is_signed)
    div.set_as_output("quotient")
    rem.set_as_output("remainder")

