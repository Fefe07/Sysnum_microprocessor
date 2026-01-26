################################################################################
#####################   REGISTERS FOR PIPELINED CPU   #########################
################################################################################
# Les registres sont lus pendant ID et écrits pendant WB
# version de reg sans PC et branchements pour pipeline

from lib_carotte import *
from typing import *

from log_unit import concat
from mux import mux
from demux import demux

def register(data_in, write_en):
    assert write_en.bus_size == 1
    n = data_in.bus_size
    reg = Reg(Defer(n, lambda: reg_in))
    reg_in = Mux(write_en, reg, data_in)
    return reg


def registers_pipeline(write_addr, write_data, read_addrs, write_en):
    allow_ribbon_logic_operations(True)
    
    n = write_data.bus_size
    nb_regs = 32
    
    write_en_signals = demux(write_addr, write_en)
   
    # x0 = 0
    # x1-x31 = registres normaux
    regs = [Constant(n * "0")]  # x0 = 0
    for i in range(1, nb_regs):
        regs.append(register(write_data, write_en_signals[i]))
    
    all_regs = concat(regs)
    read_values = []
    for addr in read_addrs:
        read_values.append(mux(addr, all_regs))
    
    return read_values


def main():
    n = 32
    write_addr = Input(5)
    write_data = Input(n)
    read_addr1 = Input(5)
    read_addr2 = Input(5)
    write_en = Input(1)
    
    vals = registers_pipeline(write_addr, write_data, [read_addr1, read_addr2], write_en)
    vals[0].set_as_output("rs1_val")
    vals[1].set_as_output("rs2_val")

# Exemple:
# Step 1 :
# write_addr ? 3
# 3  u3 (0b00011)
# write_data ? 123
# 123  u123 (0b00000000000000000000000001111011)
# read_addr1 ? 3
# 3  u3 (0b00011)
# read_addr2 ? 4
# 4  u4 (0b00100)
# write_en ? 1
# -1  u1 (0b1)
# => rs1_val = 0  u0 (0b00000000000000000000000000000000)
# => rs2_val = 0  u0 (0b00000000000000000000000000000000)
# Step 2 :
# write_addr ? 4
# 4  u4 (0b00100)
# write_data ? 200
# 200  u200 (0b00000000000000000000000011001000)
# read_addr1 ? 3
# 3  u3 (0b00011)
# read_addr2 ? 4
# 4  u4 (0b00100)
# write_en ? 1
# -1  u1 (0b1)
# => rs1_val = 123  u123 (0b00000000000000000000000001111011)
# => rs2_val = 0  u0 (0b00000000000000000000000000000000)
# Step 3 :
# write_addr ? 0
# 0  u0 (0b00000)
# write_data ? 0
# 0  u0 (0b00000000000000000000000000000000)
# read_addr1 ? 3
# 3  u3 (0b00011)
# read_addr2 ? 4
# 4  u4 (0b00100)
# write_en ? 0
# 0  u0 (0b0)
# => rs1_val = 123  u123 (0b00000000000000000000000001111011)
# => rs2_val = 200  u200 (0b00000000000000000000000011001000)
