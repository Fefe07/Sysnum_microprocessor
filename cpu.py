################################################################################
#################        CENTRAL PROCESSING UNIT         #######################
################################################################################

from lib_carotte import *
from typing import *

from arith_unit import adder
from regs import registers
from mux import mux
from alu import alu
from log_unit import b_or

def decoder(instruction):
    x = instruction
    sizes = [5, 5, 5, 8, 3, 1, 1, 1, 3]
    positions = [32 for _ in range(len(sizes) + 1)]
    for i in range(len(sizes)):
        positions[i+1] = positions[i] - sizes[i]
    assert positions[-1] == 0
    return tuple(x[positions[i+1]:positions[i]] for i in range(len(sizes)))

def cpu():
    allow_ribbon_logic_operations(True)
    
    n = 32
    data_size = n
    instruction_size = 32
    rom_addr_size = 10 
    ram_addr_size = 10
    # reg_addr_size = 5

    branch_en = Defer(1, lambda: condition_met )
    data_in = Defer(n, lambda: new_rd) 
    (vs1, vs2, pc) = registers(Defer(5, lambda:rd), data_in, [Defer(5, lambda:rs1), Defer(5, lambda:rs2)], branch_en)
    instruction = ROM(rom_addr_size, instruction_size, pc[:rom_addr_size])
    rs1,rs2,rd,imm,op,is_imm, write_to_ram, read_from_ram, condition = decoder(instruction)
    
    completed_imm = imm + Constant((n-imm.bus_size)*"0")
    is_branch = b_or(condition)
    va = mux(is_imm, vs1+completed_imm)
    vb = vs2
    result, eq, lt, ltu = alu(va, vb, op)
    condition_met = condition[0] ^ (mux(condition[1:], Constant("0")+eq+lt+ltu))
    data = RAM(ram_addr_size, data_size, result[:ram_addr_size], write_to_ram, result[:ram_addr_size], vs1)
    new_rd = mux(read_from_ram, mux(is_branch, result+completed_imm)+data)
    return va, vb, pc, condition_met

def main() :
    v1,v2, pc, is_jmp = cpu()
    v1.set_as_output("v1")
    v2.set_as_output("v2")
    pc.set_as_output("pc")
    is_jmp.set_as_output("jmp")
    # ra.set_as_output("ra")

