################################################################################
######################      LOGIC UNIT         #################################
################################################################################

from lib_carotte import *
from typing import *

from arith_unit import arith_unit
from log_unit import b_or 

def flags(a, b, res_sub, carry):
    n = a.bus_size
    ZF = ~b_or(res_sub) # zero flag 
    CF = ~carry # borrow flag 
    SF = res_sub[n-1] # sign flag
    NF = (SF | (a[n-1] & ~b[n-1]) ) & (a[n-1] | ~b[n-1]) # negative flag 
    return ZF, CF, NF

