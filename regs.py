################################################################################
#####################        REGISTERS         #################################
################################################################################


from lib_carotte import *
from typing import *

from log_unit import concat
from mux import mux
from demux import demux
from arith_unit import adder

def register(data_in, write_en):
    assert write_en.bus_size == 1
    n = data_in.bus_size
    reg = Reg(Defer(n, lambda : reg_in))
    reg_in = Mux(write_en, reg, data_in)
    return reg

def registers(write_select, data_in, read_select_list, is_branch, is_jmp ) :
    assert is_jmp.bus_size == is_branch.bus_size == 1
    for read_sel_i in read_select_list:
        assert write_select.bus_size == read_sel_i.bus_size
    n = data_in.bus_size
    
    nb_bit_sel_reg = write_select.bus_size
    nb_regs = 2**nb_bit_sel_reg 
    reg_size = data_in.bus_size

    write_en_signals = demux(write_select, Constant("1"))
    assert len(write_en_signals) == nb_regs
    
    pc = Reg(Defer(n, lambda: actual_next_pc))

    next_pc, _ = adder(pc, Mux(is_branch, Constant("001"+(n-3)*"0"), data_in), Constant("0"))
    actual_next_pc = Mux(write_en_signals[nb_regs-1] | is_jmp , next_pc, data_in)
    regs = [Constant(reg_size*"0")] + [register(Mux(is_jmp, data_in,next_pc), write_en_signals[i]) for i in range(1, nb_regs-1)] + [ pc ] 
     
    return tuple([mux(read_select, concat(regs)) for read_select in read_select_list] + [pc])



def main():
    n = 8
    data_in = Input(n)
    write_select = Input(3)
    read_select1 = Input(3)
    read_select2 = Input(3)
    branch_en = Input(1)
    regs = registers(write_select, data_in, [read_select1, read_select2], branch_en)
    for i in range(len(regs)-1) :
        regs[i].set_as_output("r"+str(i+1))
    regs[-1].set_as_output("pc")

# Exemple :
# Step 1 :
# data_in ? 10
# 10  u10 (0b00001010)
# write_select ? 1
# 1  u1 (0b001)
# read_select1 ? 1
# 1  u1 (0b001)
# read_select2 ? 7
# -1  u7 (0b111)
# branch_en ? 0
# 0  u0 (0b0)
# => r1 = 0  u0 (0b00000000)
# => r2 = 0  u0 (0b00000000)
# => pc = 0  u0 (0b00000000)
# Step 2 :
# data_in ? 20
# 20  u20 (0b00010100)
# write_select ? 7
# -1  u7 (0b111)
# read_select1 ? 1
# 1  u1 (0b001)
# read_select2 ? 2
# 2  u2 (0b010)
# branch_en ? 0
# 0  u0 (0b0)
# => r1 = 10  u10 (0b00001010)
# => r2 = 0  u0 (0b00000000)
# => pc = 1  u1 (0b00000001)
# Step 3 :
# data_in ? 30
# 30  u30 (0b00011110)
# write_select ? 0
# 0  u0 (0b000)
# read_select1 ? 7
# -1  u7 (0b111)
# read_select2 ? 1
# 1  u1 (0b001)
# branch_en ? 0
# 0  u0 (0b0)
# => r1 = 20  u20 (0b00010100)
# => r2 = 10  u10 (0b00001010)
# => pc = 20  u20 (0b00010100)
# Step 4 :
# data_in ? 0
# 0  u0 (0b00000000)
# write_select ? 0
# 0  u0 (0b000)
# read_select1 ? 0
# 0  u0 (0b000)
# read_select2 ? 1
# 1  u1 (0b001)
# branch_en ? 0
# 0  u0 (0b0)
# => r1 = 0  u0 (0b00000000)
# => r2 = 10  u10 (0b00001010)
# => pc = 21  u21 (0b00010101)
# Step 5 :
# data_in ? 30
# 30  u30 (0b00011110)
# write_select ? 5
# -3  u5 (0b101)
# read_select1 ? 5
# -3  u5 (0b101)
# read_select2 ? 1
# 1  u1 (0b001)
# branch_en ? 1
# -1  u1 (0b1)
# => r1 = 0  u0 (0b00000000)
# => r2 = 10  u10 (0b00001010)
# => pc = 22  u22 (0b00010110)
# Step 6 :
# data_in ? 40
# 40  u40 (0b00101000)
# write_select ? 7
# -1  u7 (0b111)
# read_select1 ? 5
# -3  u5 (0b101)
# read_select2 ? 7
# -1  u7 (0b111)
# branch_en ? 1
# -1  u1 (0b1)
# => r1 = 23  u23 (0b00010111)
# => r2 = 30  u30 (0b00011110)
# => pc = 30  u30 (0b00011110)
# Step 7 :
# data_in ? 0   
# 0  u0 (0b00000000)
# write_select ? 5
# -3  u5 (0b101)
# read_select1 ? 0
# 0  u0 (0b000)
# read_select2 ? 5
# -3  u5 (0b101)
# branch_en ? 0
# 0  u0 (0b0)
# => r1 = 0  u0 (0b00000000)
# => r2 = 23  u23 (0b00010111)
# => pc = 40  u40 (0b00101000)
# Step 8 :
# data_in ? 