################################################################################
#########################        MULTIPLIER         ############################
################################################################################

from lib_carotte import *
from typing import *

from arith_unit import adder, arith_unit
from log_unit import clone

def multipliy(a, b):
    allow_ribbon_logic_operations(True)
    if a.bus_size < b.bus_size :
        return multipliy(b,a)
    assert a.bus_size >= b.bus_size
    if b.bus_size == 1 :
        return clone( a.bus_size, b) & a 
    x1 = multipliy(a[0], b) 
    x2 = Constant("0")+multipliy(a[1:], b) 
    assert x2.bus_size > x1.bus_size
    x1_c = x1 + Constant((x2.bus_size - x1.bus_size) * "0")
    (s, overflow) = adder(x1_c, x2 , Constant("0"))
    if a.bus_size == 2 :
        s = s + overflow
    assert s.bus_size == a.bus_size+b.bus_size
    return s

def multiplier(a,b,a_signed, b_signed):
    assert a.bus_size == b.bus_size and a.bus_size > 2
    assert b_signed.bus_size == a_signed.bus_size == 1
    n = a.bus_size

    xa = Mux(a_signed, b, a)
    xb = Mux(a_signed, a, b)
    only_a_signed = a_signed ^ b_signed 
    both_signed = a_signed & b_signed 

    sa = xa[n-1]
    sb = xb[n-1]
    la = xa[:n-1]
    lb = xb[:n-1]
    
    low = multipliy(la, lb)
    s_mid, carry = arith_unit(clone(n-1,sb) & la, clone(n-1,sa) & lb , only_a_signed )
    overflow = carry ^ only_a_signed
    middle = s_mid+overflow
    s = sa & sb
    exterior_part = low + s + (s & only_a_signed)
    middle_part = Constant((n-1)*"0") + middle + (overflow & only_a_signed)
    
    res, _ =  arith_unit(exterior_part, middle_part, both_signed)
    assert res.bus_size == 2*n
    return res

def main():
    n = 8
    a = Input(n)
    b = Input(n)
    a_signed = Constant("0")
    b_signed = Constant("0")
    x = multiplier(a,b,a_signed, b_signed)
    x.set_as_output("r")