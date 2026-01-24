################################################################################
######################        FORWARDING        ################################
################################################################################

# IF → [Reg] → ID → [Reg] → EX → [Reg] → MEM → [Reg] → WB

from lib_carotte import *
from typing import *

from log_unit import b_or, b_and, clone
from mux import mux

def forward(rs_addr, ex_mem_rd_addr, mem_wb_rd_addr, ex_mem_write_en, mem_wb_write_en):
    allow_ribbon_logic_operations(True)
    n = rs_addr.bus_size
    
    rs_eq_ex_mem = ~b_or(rs_addr ^ ex_mem_rd_addr)   # rs == ex_mem_rd ?
    rs_eq_mem_wb = ~b_or(rs_addr ^ mem_wb_rd_addr)   # rs == mem_wb_rd ?
    rs_not_zero = b_or(rs_addr)                      # rs != x0
    
    # priorité EX/MEM
    forward_ex_mem = rs_eq_ex_mem & ex_mem_write_en & rs_not_zero
    forward_mem_wb = rs_eq_mem_wb & mem_wb_write_en & rs_not_zero & ~forward_ex_mem
    
    return forward_ex_mem + forward_mem_wb # out -> 2 bits


def forward_mux(rs_value, ex_mem_result, mem_wb_result, forward_sel):
    allow_ribbon_logic_operations(True)
        
    sel0 = forward_sel[0]
    sel1 = forward_sel[1]
    
    # sel = 01 → ex_mem_result
    # sel = 10 → mem_wb_result
    # sel = 00 → rs_value
    temp = Mux(sel0, rs_value, ex_mem_result)
    result = Mux(sel1, temp, mem_wb_result)
    
    return result

def main():
    rs_addr = Input(5)
    ex_mem_rd = Input(5)
    mem_wb_rd = Input(5)
    ex_mem_wen = Input(1)
    mem_wb_wen = Input(1)
    
    forward_sel = forward(rs_addr, ex_mem_rd, mem_wb_rd, ex_mem_wen, mem_wb_wen)
    forward_sel.set_as_output("forward_sel")

# exemples:
# Step 1 :
#rs_addr ? 0b00001
#ex_mem_rd ? 0b00010
#mem_wb_rd ? 0b00011
#ex_mem_wen ? 0b1
#mem_wb_wen ? 0b1
#=> forward_sel = 0  u0 (0b00)
# Step 2 :
# rs_addr    ? 0b00101
# ex_mem_rd  ? 0b00101
# mem_wb_rd  ? 0b00011
# ex_mem_wen ? 0b1
# mem_wb_wen ? 0b1
# => forward_sel = 1 (0b01)
# Step 3 :
# rs_addr    ? 0b00111
# ex_mem_rd  ? 0b00010
# mem_wb_rd  ? 0b00111
# ex_mem_wen ? 0b1
# mem_wb_wen ? 0b1
# => forward_sel = 2 (0b10)
