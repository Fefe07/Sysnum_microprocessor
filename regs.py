################################################################################
#####################        REGISTERS         #################################
################################################################################


from lib_carotte import *
from typing import *

from log_unit import concat
from mux import mux
from demux import demux

def register(data_in, write_en):
    assert write_en.bus_size == 1
    n = data_in.bus_size
    reg = concat([ Reg(Defer(1, lambda i=i : reg_in[i])) for i in range(n) ])
    reg_in = mux(write_en, reg+data_in)
    return reg

def registers(write_select, data_in, read_select_list) :
    for read_sel_i in read_select_list:
        assert write_select.bus_size == read_sel_i.bus_size
    nb_bit_sel_reg = write_select.bus_size
    nb_regs = 2**nb_bit_sel_reg
    reg_size = data_in.bus_size
    write_en_signals = demux(write_select, Constant("1"))
    assert len(write_en_signals) == nb_regs
    regs = [Constant(reg_size*"0")] +[register(data_in, write_en_signals[i]) for i in range(1, nb_regs)]
    return [mux(read_select, concat(regs)) for read_select in read_select_list]

def main():
    n = 8
    data_in = Input(n)
    write_select = Input(3)
    read_select = Input(3)
    # read_select2 = Input(3)
    regs = registers(write_select, data_in, [read_select])
    for i in range(len(regs)) :
        regs[i].set_as_output("r"+str(i+1))

# Exemple :
# Step 1 :
# data_in ? 67
# write_select ? 2
# read_select ? 2
# => r1 = 0 (0b00000000)
# Step 2 :
# data_in ? 32
# write_select ? 2
# read_select ? 2
# => r1 = 67 (0b01000011)
# Step 3 :
# data_in ? 36
# write_select ? 5
# read_select ? 2
# => r1 = 32 (0b00100000)
# Step 4 :
# data_in ? 31
# write_select ? 0
# read_select ? 5
# => r1 = 36 (0b00100100)
# Step 5 :
# data_in ? 123
# write_select ? 1
# read_select ? 0
# => r1 = 0 (0b00000000)
# Step 6 :
# data_in ? 0
# write_select ? 0
# read_select ? 2
# => r1 = 32 (0b00100000)