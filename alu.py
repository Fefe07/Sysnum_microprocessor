################################################################################
###############        ARITHMETIC AND LOGIC UNIT         #######################
################################################################################

from lib_carotte import *
from typing import *

from arith_unit import arith_unit, adder 
from mux import mux
from log_unit import b_or
from flags import flags

# opérations actuelles ( va sûrement changer ! )
# 0 -> add
# 1 -> sub
# 2 -> and
# 3 -> or
# 4 -> xor
# 5 -> slt
# 6 -> 0 
# 7 -> sltu
def alu(a, b, op):
    assert a.bus_size == b.bus_size
    assert op.bus_size == 3
    allow_ribbon_logic_operations(True)
    n = a.bus_size

    add_sub, carry = arith_unit( a, b, op[0] ) 
    EQ, LTU, LT = flags(a, b, add_sub, carry)
    and_or  = Mux(op[0], (a & b), (a|b) )
    xor_slt = Mux(op[0], (a ^ b), LT + Constant((n-1)*"0") )
    sltu = LTU + Constant((n-1)*"0")
    zero_sltu = Mux(op[0], Constant(n*"0"), sltu )
    # sltu.set_as_output("sltu")
    res = mux(op[2] + op[1], add_sub+and_or+xor_slt+zero_sltu)

    return res, EQ, LTU, LT

def main() -> None:
    '''Entry point of this example'''
    allow_ribbon_logic_operations(True)

    n = 4
    a, ov = adder(Reg(Defer(n, lambda: a)), Constant(n*"0"), Constant("1"))
    b, _ = adder(Reg(Defer(n, lambda: b)), Constant(n*"0"), ov)
    op = Constant("100")
    res, eq, ltu, lt = alu(a, b, op)
    a.set_as_output("a")
    b.set_as_output("b")
    res.set_as_output("res")
    eq.set_as_output("eq")
    lt.set_as_output("lt")
    ltu.set_as_output("ltu")
    

# Exemples:

# add :
# a ? 120
# b ? 35
# op ? 0
# => r = 155 (0b10011011)

# sub :
# a ? 120
# b ? 30
# op ? 1
# => r = 90 (0b01011010)

# and :
# a ? 0b11001100
# b ? 0b10101001
# op ? 2
# => r = 136 (0b10001000)

# or :
# a ? 0b11001100
# b ? 0b10101001
# op ? 3
# => r = 237 (0b11101101)

# not :
# a ? 0b11001100 
# b ? 0b10101001
# op ? 4
# => r = 86 (0b01010110)

# xor :
# a ? 0b11001100
# b ? 0b10101001
# op ? 5
# => r = 101 (0b01100101)

# op 6 :
# a ? 0b11001100
# b ? 0b10101001
# op ? 6
# => r = 0 (0b00000000)

# op 7 :
# a ? 0b11001100
# b ? 0b10101001
# op ? 7
# => r = 0 (0b00000000)