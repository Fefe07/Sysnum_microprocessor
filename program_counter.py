################################################################################
###############        PROGRAM COUNTER         #################################
################################################################################


from lib_carotte import *
from typing import *

from mux import mux
from arith_unit import adder
from log_unit import concat

def program_counter(branch_in, branch_en) :
    assert branch_en.bus_size == 1
    n = branch_in.bus_size
    pc = concat([Reg(Defer(1, lambda i = i : data_in[i]))  for i in range(n) ])
    next_pc, overflow = adder(pc, Constant("1"+(n-1)*"0"), Constant("0"))
    data_in = mux(branch_en, next_pc+branch_in)
    return pc

def main():
    n = 8
    branch_in = Input(n)
    branch_en = Input(1)
    program_counter(branch_in, branch_en).set_as_output("pc") 

# Exemple :
# Step 1 :
# branch_in ? 23
# branch_en ? 1
# => pc = 0 (0b00000000) # Je sais pas si le branch doit agir à la clock suivante ou instantannément
# Step 2 :
# branch_in ? 21
# branch_en ? 0
# => pc = 23 (0b00010111)
# Step 3 :
# branch_in ? 21
# branch_en ? 0
# => pc = 24 (0b00011000)
# Step 4 :
# branch_in ? 21
# branch_en ? 0
# => pc = 25 (0b00011001)