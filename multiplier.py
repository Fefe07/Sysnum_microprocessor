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

def multiplier(a,b,is_signed):
    assert a.bus_size == b.bus_size and a.bus_size > 2
    assert is_signed.bus_size == 1
    n = a.bus_size

    sa = a[n-1]
    sb = b[n-1]
    ra = a[:n-1]
    rb = b[:n-1]
    low = multipliy(ra, rb)
    (s_mid,overflow) = adder(clone(n-1,sb) & ra, clone(n-1,sa) & rb , Constant("0"))
    middle = s_mid+overflow
    s = sa & sb

    positive_part = low + s + Constant("0") 
    signed_part = Constant((n-1)*"0") + middle + Constant("0")
    (res, overflow) =  arith_unit(positive_part, signed_part, is_signed)
    return res

def main():
    a = Input(8)
    b = Input(8)
    s = Input(1)
    x = multiplier(a,b,s)
    x.set_as_output("r")