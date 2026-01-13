################################################################################
#################        CENTRAL PROCESSING UNIT         #######################
################################################################################

from lib_carotte import *
from typing import *

from arith_unit import adder
from regs import registers
from mux import mux
from alu import alu
from log_unit import b_or, clone
from multiplier import multiplier

def extend_sign(x):
    n = x.bus_size
    return  x + clone(32-n, x[n-1])

def decoder(x):
    funct7 = x[25:32]
    rs2 = x[20:25] # A CHANGER POUR U et J type
    rs1 = x[15:20]
    rd_bits = x[7:12]
    funct3 = x[12:15]
    opcode = x[0:7]

    imm_I = extend_sign(x[20:32])
    imm_S = extend_sign(x[7:12]+x[25:32])
    imm_B = extend_sign(x[7:12]+x[25:32])
    imm_U = Constant(12*"0") + x[12:32]
    imm_J = extend_sign(x[12:32])

    is_jmp = opcode[0]
    is_branch = opcode[1]
    is_imm = opcode[2]
    read_from_ram = opcode[3]
    write_to_ram = opcode[4]
    
    op = Mux(is_branch, funct3, Constant("100"))
    condition = Mux(is_branch, Mux(is_jmp, Constant("000"),Constant("001")), funct3)
    rd = Mux(is_branch | write_to_ram, rd_bits, Constant("00000"))
    is_mult = (~is_imm) & funct7[0]

    imm = Mux(is_jmp | is_branch, Mux(write_to_ram, imm_I, imm_S), Mux(is_branch, imm_J, imm_B))
    return rs1, rs2, rd, imm, op, is_imm, write_to_ram, read_from_ram, condition, is_mult

def cpu():
    allow_ribbon_logic_operations(True)
    DISABLE_MULTIPLICATION = False # ça peut ralentir significativement la compilation 
    n = 32
    data_size = n
    instruction_size = 32
    rom_addr_size = 10 
    ram_addr_size = 10
    # reg_addr_size = 5

    vs1, vs2, pc = registers(Defer(5, lambda:rd), Defer(n, lambda: data_in_regs), [Defer(5, lambda:rs1), Defer(5, lambda:rs2)], Defer(1, lambda: condition_met ))
    instruction = ROM(rom_addr_size, instruction_size, pc[:rom_addr_size])
    rs1, rs2, rd, imm, op, is_imm, write_to_ram, read_from_ram, condition, is_mult = decoder(instruction)
    
    is_conditional_branch = b_or(condition[1:])
    va = vs1
    vb = mux(is_imm, vs2 + imm) 

    alu_result, eq, ltu, lt = alu(va, vb, op)
    mult_res = mux(op[0],  multiplier(va, vb, op[1], op[2]) if not DISABLE_MULTIPLICATION else Constant(64*"0") )
    result = Mux(is_mult, alu_result, mult_res)
    # conditions : NEVER = 000  ALWAYS = 001  LT = 010  GE = 011  EQ = 100  NEQ = 101  LTU = 110  GEU = 111       
    condition_met = condition[0] ^ (mux(condition[1:], Constant("0")+eq+lt+ltu))
    # reads from /writes vs2 to the adress result (modulo the size of the ram)  - it writes if write_to_ram = 1
    data_from_ram = RAM(ram_addr_size, data_size, result[:ram_addr_size], write_to_ram, result[:ram_addr_size], vs2)
    data_in_regs = mux(read_from_ram, mux(is_conditional_branch, result+imm) + data_from_ram)
    
    return rd, va, vb, pc, condition_met, data_in_regs 

def main() :
    rd, v1,v2, pc, is_jmp, result = cpu()
    v1.set_as_output("v1")
    v2.set_as_output("v2")
    pc.set_as_output("pc")
    is_jmp.set_as_output("jmp")
    rd.set_as_output("rd")
    result.set_as_output("alu_res")

