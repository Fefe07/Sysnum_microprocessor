from instructions import *

prog_clock = [
    load(1,0,8),
    mov_reg(7,1),
    mov_imm(3,1),
    mov_imm(4,0),
    load(5,0,8),
    branch("eq",7, 5, -4),
    op_reg("sub", 6, 5, 1),
    store(0,4,6),
    store(0,0,3),
    mov_reg(7,5),
    branch("always", 0, 0, -6*4)
]


print_prog(prog_clock)
print()
