from instructions import *

# Programme calculant la suite de fibonacci jusqu'à ce qu'elle dépasse 20
prog_fibo = [
    mov_imm(3, 1),
    mov_imm(1, 1),
    mov_imm(2, 1),
    mov_reg(4, 1),
    mov_reg(1, 2),
    mov_reg(2, 4),
    op_reg("add", 1, 1, 2),
    op_imm("slt", 4, 1, 20),
    store(0,0,1),
    branch("eq", 4, 3, -6*4)]

prog_fibo2 = [
    mov_imm(3, 20),
    mov_imm(1, 1),
    mov_imm(2, 1),
    mov_reg(4, 1),
    mov_reg(1, 2),
    mov_reg(2, 4),
    op_reg("add", 1, 1, 2),
    store(3, -4, 1),
    load(1, 0, 16), 
    branch("ltu", 1, 3, -6*4)]

prog_fact = [
    mov_imm(1, -20),
    mov_imm(2, -1),
    mov_imm(3, -1),  
    op_reg("mulhsu",4, 1, 2),
    op_reg("mul", 2, 2, 1),
    op_reg("mul", 3, 3, 1),
    op_reg("add", 3, 3, 4),
    op_imm("add", 1, 1, 1),
    branch("neq", 1, 0, -5*4)
]

prog_test_jmp = [
    mov_imm(31, 20),
    mov_imm(1, 1),
    mov_imm(2, 1),
    mov_reg(4, 1),
    mov_reg(1, 2),
    mov_reg(2, 4),
    op_reg("add", 1, 1, 2),
    store(31, -4, 1),
    load(1, 0, 16), 
    branch("ltu", 1, 31, -6*4),
    jump(5, 50*4),
    '0',
    '0',
    mov_reg(6, 6)
    ]+ (['0']*46) +[
    jump_reg(6, 5, 2*4) 
    ]

prog_test_alu = [
    mov_imm(1, -20),
    mov_imm(2, 23),
    op_imm("sll", 0, 1, 23),
    op_reg("add", 0, 1, 2),
    op_reg("sll", 0, 1, 2),
    op_reg("sub", 0, 1, 2),
    op_reg("and", 0, 1, 2),
    op_reg("or", 0, 1, 2),
    op_reg("xor", 0, 1, 2),
    op_reg("slt", 0, 1, 2),
    op_reg("srl", 0, 1, 2),
    op_reg("sra", 0, 1, 2),
    op_reg("sltu", 0, 1, 2),
    lui(0, 5),
    auipc(0, 5)
 ]

prog_test_muldiv = [
    mov_imm(1, -105),
    mov_imm(2, -10),
    op_reg("mul", 0, 1, 2),
    op_reg("mulh", 0, 1, 2),
    op_reg("mulhu", 0, 1, 2),
    op_reg("mulhsu", 0, 1, 2),
    op_reg("div", 0, 1, 2),
    op_reg("divu", 0, 1, 2),
    op_reg("rem", 0, 1, 2),
    op_reg("remu", 0, 1, 2)
]

test_granularity = [
    mov_imm(1,-1),
    store(0, 2, 1),
    branch("always",0,0,-4)
]

print_prog(test_granularity)
print()
