################################################################################
###################    CPU PIPELINE                     ########################
################################################################################
# IF → [Reg] → ID → [Reg] → EX → [Reg] → MEM → [Reg] → WB

from lib_carotte import *
from typing import *

from arith_unit import adder
from regs import register, registers
from mux import mux
from alu import alu
from log_unit import b_or, clone
from hazards import hazard_detection
from forwarding import forward, forward_mux

def extend_sign(x):
    n = x.bus_size
    return x + clone(32-n, x[n-1])

def decoder(x):
    funct7 = x[25:32]
    rs2 = x[20:25]
    rs1_bits = x[15:20]
    rd_bits = x[7:12]
    funct3 = x[12:15]
    opcode = x[0:7]

    imm_I = extend_sign(x[20:32])
    imm_S = extend_sign(x[7:12]+x[25:32])
    imm_B = extend_sign(x[7:12]+x[25:32])
    imm_U = Constant(12*"0") + x[12:32]
    imm_J = extend_sign(x[12:32])

    jmp_kind = opcode[0:2] # jal, jalr 
    is_imm = opcode[2]
    read_from_ram = opcode[3]
    write_to_ram = opcode[4]
    is_type_u = opcode[5]
    is_auipc = opcode[6]
    rs1_u = clone(5, is_auipc) # refers to register pc or 0 
    is_branch = jmp_kind[0] & ~jmp_kind[1] #jmp_kind = 01 -> branch
    is_jmp = jmp_kind[1] # jmp_kind = 10 or 11  ->  jalr, jal
    
    
    op = Mux(jmp_kind[0] | is_type_u , funct3, Mux(is_branch, Constant("000") ,Constant("100")))
    condition = Mux(is_branch, Constant("000"), funct3)
    rd = Mux( is_branch | write_to_ram, rd_bits, Constant(5*"0"))
    is_muldiv = (~is_imm) & funct7[0]
    op_option = funct7[5] | is_branch # | is_branch c'est pour forcer la soustraction lors d'un test de saut conditionnel, mais on en a pas besoin car seuls les flags nous intéresse, et les flags sont mis dès que op[0] = 1
    rs1_not_u = Mux(jmp_kind[0] & jmp_kind[1], rs1_bits, Constant(5*"1")) 
    rs1 = Mux(is_type_u, rs1_not_u, rs1_u)
    imm = Mux( is_type_u,  Mux(jmp_kind[0], Mux(write_to_ram, imm_I, imm_S), Mux(is_branch, imm_J, imm_B)), imm_U)
    return rs1, rs2, rd, imm, op, is_imm, write_to_ram, read_from_ram, condition, is_muldiv, is_jmp, is_branch, op_option


def cpu_pipeline():
    allow_ribbon_logic_operations(True)
    
    n = 32
    rom_addr_size = 10
    ram_addr_size = 10
    
    # IF
    pc = Reg(Defer(n, lambda: next_pc))
    four = Constant("00100" + "0"*27)  # 4 en little-endian bit
    pc_plus_4, _ = adder(pc, four, Constant("0"))
    
    instruction = ROM(rom_addr_size, n, pc[2:rom_addr_size+2])
    
    rs1_addr, rs2_addr, rd_addr, imm, op, is_imm, write_to_ram, read_from_ram, \
        condition, is_muldiv, is_jmp, is_branch, op_option = decoder(instruction)

    # Hazard detection sur les IF
    stall = hazard_detection(
        rs1_addr, rs2_addr, 
        Defer(5, lambda: id_ex_rd), 
        Defer(1, lambda: id_ex_read_from_ram)
        )
    flush = Defer(1, lambda: branch_taken)
    not_stall = ~stall
    bubble = stall | flush
    
    # IF/ID
    if_id_pc = register(pc, not_stall)
    if_id_rs1_addr = register(rs1_addr, not_stall)
    if_id_rs2_addr = register(rs2_addr, not_stall)
    if_id_rd_addr = register(rd_addr, not_stall)
    if_id_imm = register(imm, not_stall)
    if_id_op = register(op, not_stall)
    if_id_op_option = register(op_option, not_stall)
    if_id_is_imm = register(is_imm, not_stall)
    if_id_read_from_ram = register(read_from_ram, not_stall)
    if_id_write_to_ram = register(write_to_ram, not_stall)
    if_id_is_branch = register(is_branch, not_stall)
    if_id_condition = register(condition, not_stall)
    
    # ID
    reg_write_en = Defer(1, lambda: wb_write_en)
    reg_write_addr = Defer(5, lambda: wb_rd)
    reg_write_data = Defer(n, lambda: wb_data)
    actual_write_addr = Mux(Defer(1, lambda: wb_write_en), Constant("00000"), Defer(5, lambda: wb_rd))
    rs1_val, rs2_val, _ = registers(
    actual_write_addr, Defer(n, lambda: wb_data),
    [if_id_rs1_addr, if_id_rs2_addr],
    Constant("0"), Constant("0")
    )
    
    # ID/EX
    nop_rd = Constant("00000")
    nop_bit = Constant("0")
    
    id_ex_pc = Reg(if_id_pc)
    id_ex_rs1_val = register(rs1_val, Constant("1"))
    id_ex_rs2_val = register(rs2_val, Constant("1"))
    id_ex_rs1_addr = register(if_id_rs1_addr, Constant("1"))
    id_ex_rs2_addr = register(if_id_rs2_addr, Constant("1"))
    id_ex_rd = register(Mux(bubble, if_id_rd_addr, nop_rd), Constant("1"))
    id_ex_imm = register(if_id_imm, Constant("1"))
    id_ex_op = register(if_id_op, Constant("1"))
    id_ex_op_option = register(if_id_op_option, Constant("1"))
    id_ex_is_imm = register(if_id_is_imm, Constant("1"))
    id_ex_read_from_ram = register(Mux(bubble, if_id_read_from_ram, nop_bit), Constant("1"))
    id_ex_write_to_ram = register(Mux(bubble, if_id_write_to_ram, nop_bit), Constant("1"))
    id_ex_is_branch = register(Mux(bubble, if_id_is_branch, nop_bit), Constant("1"))
    id_ex_condition = register(if_id_condition, Constant("1"))

    # EX et forwarding
    forward_a = forward(
        id_ex_rs1_addr,
        Defer(5, lambda: ex_mem_rd),
        Defer(5, lambda: wb_rd),
        Defer(1, lambda: ex_mem_write_en),
        Defer(1, lambda: wb_write_en)
        )
    forward_b = forward(
        id_ex_rs2_addr,
        Defer(5, lambda: ex_mem_rd),
        Defer(5, lambda: wb_rd),
        Defer(1, lambda: ex_mem_write_en),
        Defer(1, lambda: wb_write_en)
        )
    
    va = forward_mux(
        id_ex_rs1_val,
        Defer(n, lambda: ex_mem_alu_result),
        Defer(n, lambda: wb_data),
        forward_a
        )
    vb_from_reg = forward_mux(
        id_ex_rs2_val,
        Defer(n, lambda: ex_mem_alu_result),
        Defer(n, lambda: wb_data),
        forward_b
        )
    vb = Mux(id_ex_is_imm, vb_from_reg, id_ex_imm)
    
    result, eq, ltu, lt = alu(va, vb, id_ex_op, id_ex_op_option)
    condition_met = id_ex_condition[0] ^ (mux(id_ex_condition[1:], Constant("0") + eq + lt + ltu))
    branch_taken = condition_met & id_ex_is_branch
    
    # EX/MEM
    ex_mem_alu_result = register(result, Constant("1"))
    ex_mem_rs2_val = register(vb_from_reg, Constant("1"))
    ex_mem_rd = register(id_ex_rd, Constant("1"))
    ex_mem_read_from_ram = register(id_ex_read_from_ram, Constant("1"))
    ex_mem_write_to_ram = register(id_ex_write_to_ram, Constant("1"))
    
    ex_mem_rd_not_zero = b_or(ex_mem_rd)
    ex_mem_write_en = ex_mem_rd_not_zero & ~ex_mem_write_to_ram
    
    # MEM
    data_from_ram = RAM(
        ram_addr_size, n,
        ex_mem_alu_result[2:ram_addr_size+2],
        ex_mem_write_to_ram,
        ex_mem_alu_result[2:ram_addr_size+2],
        ex_mem_rs2_val
    )
    mem_result = Mux(ex_mem_read_from_ram, ex_mem_alu_result, data_from_ram)
    
    # MEM/WB
    wb_data = register(mem_result, Constant("1"))
    wb_rd = register(ex_mem_rd, Constant("1"))
    wb_write_en = register(ex_mem_write_en, Constant("1"))

    # Next PC
    branch_target, _ = adder(id_ex_pc, id_ex_imm, Constant("0"))
    next_pc = Mux(branch_taken, branch_target, Mux(stall, pc, pc_plus_4))
    
    return (pc, pc_plus_4, instruction, result, wb_data, wb_rd, 
            stall, branch_taken, id_ex_is_branch, id_ex_rd, flush, bubble)

def main():
    (pc, pc_plus_4, instruction, result, wb_data, wb_rd,
     stall, branch_taken, is_branch, id_ex_rd, flush, bubble) = cpu_pipeline()
    
    pc.set_as_output("pc")
    pc_plus_4.set_as_output("pc_plus_4")
    instruction.set_as_output("instr")
    result.set_as_output("alu_result")
    wb_data.set_as_output("wb_data")
    wb_rd.set_as_output("wb_rd")
    stall.set_as_output("stall")
    branch_taken.set_as_output("branch_taken")
    id_ex_rd.set_as_output("id_ex_rd")
