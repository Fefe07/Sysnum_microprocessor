################################################################################
#################        CENTRAL PROCESSING UNIT         #######################
################################################################################

from lib_carotte import *
from typing import *

from arith_unit import adder
from program_counter import program_counter
from regs import registers
from mux import mux
from alu import alu

def decoder(instruction):
    x = instruction
    return x[:5],x[5:10],x[10:21], x[21:24], x[24:25]

def cpu():
    allow_ribbon_logic_operations(True)
    n = 32
    instruction_size = 32
    rom_addr_size = 5 
    branch_in = Constant(n*"0")
    branch_en = Constant("0")
    pc = program_counter(branch_in, branch_en)
    instruction = ROM(rom_addr_size, instruction_size, pc[:rom_addr_size])
    ra,rb,imm,op,is_imm = decoder(instruction)
    data_in = Defer(n, lambda:result) 
    values = registers(rb, data_in, [ra, rb])
    va = values[0]
    vb = values[1]
    completed_imm = imm + Constant((n-imm.bus_size)*"0")
    v1 = mux(is_imm, va+completed_imm)
    v2 = vb
    (result, overflow) = alu(v1, v2, op)
    return v1,v2, pc, ra 


def main() :
    v1,v2, pc, ra = cpu()
    v1.set_as_output("v1")
    v2.set_as_output("v2")
    pc.set_as_output("pc")
    ra.set_as_output("ra")

