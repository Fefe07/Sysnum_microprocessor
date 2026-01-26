################################################################################
###############        ARITHMETIC UNIT         #################################
################################################################################

from lib_carotte import *
from typing import *

from log_unit import concat


def full_adder(a: Variable, b: Variable, c: Variable) -> Tuple[Variable, Variable]:
    '''1-bit full adder'''
    tmp = a ^ b
    return (tmp ^ c, (tmp & c) | (a & b))

def adder(a: Variable, b: Variable, c_in: Variable) -> Tuple[Variable, Variable] :
    '''n-bit full adder'''
    assert a.bus_size == b.bus_size
    
    n = a.bus_size
    s,c_out = full_adder(a[0],b[0], c_in)
    for i in range(1, n):
        s_i, c_out = full_adder(a[i], b[i], c_out)
        s = s + s_i
    return (s, c_out)

def arith_unit(a, b, is_sub) :
    ''' adder and susbtractor unit '''
    # Ne prend en entrées que des entiers non signés ?
    assert a.bus_size == b.bus_size
    assert is_sub.bus_size == 1
    allow_ribbon_logic_operations(True)

    n = a.bus_size
    n_is_sub = concat(n*[is_sub])
    conditioned_not_b = b ^ n_is_sub
    s, carry = adder(a, conditioned_not_b, is_sub)
    return s, carry

def main() -> None:
    '''Entry point of this example'''
    allow_ribbon_logic_operations(True)

    n = 4
    a = Input(n)
    b = Input(n)
    c = Input(1)
    (result, carry) = arith_unit(a, b, c)
    result.set_as_output("r")
    carry.set_as_output("carry")

# Example:
# Step 1 :
# a ? 15
# b ? 3
# c ? 1
# => r = 12 (0b1100)
# => carry = 1 (0b1)
# Step 2 :
# a ? 9 
# b ? 2
# c ? 0
# => r = 11 (0b1011)
# => carry = 0 (0b0)