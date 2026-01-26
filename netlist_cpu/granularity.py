from instructions import *

test = [
    mov_imm(1,-1),
    store(0, 2, 1),
    branch("always",0,0,-4)
]

print_prog(test)
print()
