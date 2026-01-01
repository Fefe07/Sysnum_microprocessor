################################################################################
#########################        MULTIPLIER         ############################
################################################################################

from lib_carotte import *
from typing import *

from arith_unit import adder
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

def main():
    a = Input(8)
    b = Input(8)
    x = multipliy(a,b)
    x.set_as_output("r")