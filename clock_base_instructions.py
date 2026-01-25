from instructions import *

prog_clock = [
    mov_imm(1, 0),
    mov_imm(3,1),
    store(0,0,3),
    store(0,4,1),
    op_imm("add", 1,1,1),
    branch("always", 0, 0, -3*4)
]


print_prog(prog_clock)
print()
