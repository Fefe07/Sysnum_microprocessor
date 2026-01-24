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
    if a.bus_size == 1 :
        return a
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

def left_shift(a, b):
    m = b.bus_size
    n = a.bus_size
    zeros = Constant((2**(m-1))*"0")
    a2 = Mux(b[m-1],a+zeros, zeros+a)[:n]
    if m == 1 :
        return a2
    return left_shift(a2, b[:m-1])

def right_shift(a, b, sign_extend):
    m = b.bus_size
    n = a.bus_size
    curr_shift = 2**(m-1)
    
    extended_a = a+( clone(curr_shift,a[n-1] & sign_extend))
    a2 = Mux(b[m-1],extended_a[:n], extended_a[curr_shift:curr_shift+n])
    if m == 1 :
        return a2
    return right_shift(a2, b[:m-1], sign_extend)

def main() -> None :
    n = 4
    a = Input(n)
    b = Input(n)

    left_shift(a,b).set_as_output("r_lshift")
    right_shift(a,b, Constant("0")).set_as_output("r_rlshift")
    right_shift(a,b, Constant("1")).set_as_output("r_rashift")
    b_and(a).set_as_output("big_and_a")
    b_or(b).set_as_output("big_or_b")


# Example: pas à jour 
# Step 1 :
# a ? 0b1101
# b ? 0b1000
# => r_lshift_a = 10 (0b1010)
# => big_and_a = 0 (0b0)
# => big_and_b = 1 (0b1)
# Step 2 :
# a ? 0b1111
# b ? 0b0000
# => r_lshift_a = 14 (0b1110)
# => big_and_a = 1 (0b1)
# => big_and_b = 0 (0b0)
# Step 3 :
# a ? 0b0111
# b ? 0b1000
# => r_lshift_a = 14 (0b1110)
# => big_and_a = 0 (0b0)
# => big_and_b = 1 (0b1)