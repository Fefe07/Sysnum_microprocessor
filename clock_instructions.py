from instructions import *

prog_clock = [
    mov_imm(1, 0),
    mov_imm(2,0),
    store(2,0,1),
    op_imm("add", 1,1,1),
    branch("always", 0, 0, -2*4)
]
print_prog(prog_clock)
print()
