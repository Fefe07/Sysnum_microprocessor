################################################################################
######################      LOGIC UNIT         #################################
################################################################################

from lib_carotte import *
from typing import *

def concat(l):
    s = l[0]
    for x in l[1:] :
        s = s + x
    return s

def clone(n, x):
    return concat(n*[x])

def multi_binop(f_op, a):
    assert a.bus_size >= 2
    if a.bus_size == 2 :
        return f_op(a[0], a[1])
    return f_op(a[0], multi_binop(f_op, a[1:]) )

def b_and(a):
    return multi_binop(lambda x,y : x & y, a)

def b_or(a):
    return multi_binop(lambda x,y : x | y, a)

def simple_left_shift(a):
    n = a.bus_size
    return Constant("0")+a[:n-1]

def main() -> None :
    allow_ribbon_logic_operations(True)

    n = 4
    a = Input(n)
    b = Input(n)

    simple_left_shift(a).set_as_output("r_lshift_a")
    b_and(a).set_as_output("bug_and_a")
    b_or(b).set_as_output("bug_or_b")

# Example:
# Step 1 :
# a ? 0b1101
# b ? 0b1000
# => r_lshift_a = 10 (0b1010)
# => bug_and_a = 0 (0b0)
# => bug_and_b = 1 (0b1)
# Step 2 :
# a ? 0b1111
# b ? 0b0000
# => r_lshift_a = 14 (0b1110)
# => bug_and_a = 1 (0b1)
# => bug_and_b = 0 (0b0)
# Step 3 :
# a ? 0b0111
# b ? 0b1000
# => r_lshift_a = 14 (0b1110)
# => bug_and_a = 0 (0b0)
# => bug_and_b = 1 (0b1)