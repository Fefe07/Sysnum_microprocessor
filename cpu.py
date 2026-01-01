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
    sizes = [5, 5, 5, 10, 3, 1, 1, 1, 1]
    positions = [32 for _ in range(len(sizes) + 1)]
    for i in range(len(sizes)):
        positions[i+1] = positions[i] - sizes[i]
    assert positions[-1] == 0
    return (x[positions[i+1]:positions[i]] for i in range(len(sizes)))

def cpu():
    allow_ribbon_logic_operations(True)
    
    n = 32
    data_size = n
    instruction_size = 32
    rom_addr_size = 10 
    ram_addr_size = 10

    branch_in = Defer(n, lambda: result)
    branch_en = Defer(1, lambda: is_branch)
    pc = program_counter(branch_in, branch_en)
    instruction = ROM(rom_addr_size, instruction_size, pc[:rom_addr_size])
    rs1,rs2,rd,imm,op,is_imm, write_to_ram, read_from_ram, is_branch = decoder(instruction)
    data_in = Defer(n, lambda:new_rd) 
    values = registers(rd, data_in, [rs1, rs2])
    vs1 = values[0]
    vs2 = values[1]
    completed_imm = imm + Constant((n-imm.bus_size)*"0")
    va = mux(is_imm, vs1+completed_imm)
    vb = vs2
    (result, overflow) = alu(va, vb, op)
    data = RAM(ram_addr_size, data_size, result[:ram_addr_size], write_to_ram, result[:ram_addr_size], vs1)
    new_rd = mux(read_from_ram, result+data)
    return va, vb

def main() :
    v1,v2 = cpu()
    v1.set_as_output("v1")
    v2.set_as_output("v2")
    # pc.set_as_output("pc")
    # ra.set_as_output("ra")

