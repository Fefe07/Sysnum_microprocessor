def get_instruction(t, **args):
    if t == "r" :
        res = args["funct7"]+args["rs2"]+args["rs1"]+args["funct3"]+args["rd"]+args["opcode"]
    elif t == "i":
        res = args["imm_I"]+args["rs1"]+args["funct3"]+args["rd"]+args["opcode"]
    elif t == "s":
        res = args["imm_S"][0:-5]+args["rs2"]+args["rs1"]+args["funct3"]+args["imm_S"][-5:]+args["opcode"]
    elif t == "b":
        res = args["imm_B"][0:-5]+args["rs2"]+args["rs1"]+args["funct3"]+args["imm_B"][-5:]+args["opcode"]
    elif t == "u":
        res = args["imm_U"]+args["rd"]+args["opcode"]
    elif t == "j":
        res = args["imm_J"]+args["rd"]+args["opcode"]
    else :
        print("TYPE INCONNU")
    assert(len(res) == 32)
    return res

def get_number(x, size, signed):
    if signed :
        assert (-2**(size -1 ) <= x < 2**(size-1) )
    else :
        assert ( 0 <= x < 2**size)
    if not signed :
        sign = ""
        size = size + 1 
    elif x < 0 :
        x = x + 2**(size -1 )
        sign = "1"
    else :
        sign = "0"
    
    res = ""
    for _ in range(size - 1):
        res = str(x%2) + res
        x = x // 2
    assert(x == 0)
    return sign + res

def get_op(op):
    ht = {
        "add" : 0,
        "sub" : 1,
        "and" : 2,
        "or"  : 3,
        "not" : 4,
        "xor" : 5,

        "mul" : 0,
        "mulhu": 1,
        "mulhsu" : 3,
        "mulh" : 7
    }
    return get_number(ht[op], 3, False)

def get_imm(imm, size):
    return get_number(imm, size, True)

def get_reg(reg):
    return get_number(reg, 5, False) 

def get_condition(cond):
    ht = {
        "never" : "000",
        "always": "001",
        "lt"    : "010",
        "ge"    : "011",
        "eq"    : "100",
        "neq"   : "101",
        "ltu"   : "110",
        "geu"   : "111"
    }
    return ht[cond]

def strb(b):
    return ("1" if b else "0")

def get_opcode(is_jmp, is_branch, is_imm, read_from_ram, write_to_ram):
    return "00"+strb(write_to_ram)+strb(read_from_ram)+strb(is_imm)+strb(is_branch)+strb(is_jmp)

def op_imm(op, dest, src, imm):
    return get_instruction("i", imm_I = get_imm(imm, 12), rs1 = get_reg(src), rd = get_reg(dest), opcode = "0000100", funct3 = get_op(op))

def op_reg(op, dest, src1, src2):
    return get_instruction("r", rs2 = get_reg(src2), rs1 = get_reg(src1), rd = get_reg(dest), opcode = "0000000", funct7 = ("0000001" if op[:3] == "mul" else "0000000"), funct3 = get_op(op))

def branch(condition, src1, src2, addr):
    return get_instruction("b", rs2 = get_reg(src2), rs1 = get_reg(src1), opcode = "0000010", funct3 = get_condition(condition), imm_B = get_imm(addr, 12))

def mov_imm(dest, imm):
    return op_imm("add", dest, 0, imm)

def mov_reg(dest, reg):
    return op_reg("add", dest, 0, reg)

def store(base, offset, src):
    return get_instruction("s", imm_S = get_imm(offset, 12), rs2 = get_reg(src), rs1 = get_reg(base), funct3 = "000", opcode = get_opcode(False, False, True, False, True))

def load(dest, base, offset):
    return get_instruction("i", imm_I = get_imm(offset, 12), rs1 = get_reg(base), rd = get_reg(dest), funct3 = "000", opcode = get_opcode(False, False, True, True, False) )

def print_prog(p):
    for n,i in enumerate(p):
        print(n)
        print("0b"+i)

# Programme calculant la suite de fibonacci jusqu'à ce qu'elle dépasse 20
prog_fibo = [
    mov_imm(3, 20),
    mov_imm(1, 1),
    mov_imm(2, 1),
    mov_reg(4, 1),
    mov_reg(1, 2),
    mov_reg(2, 4),
    op_reg("add", 1, 1, 2),
    branch("ltu", 1, 3, 3)]

prog_fibo2 = [
    mov_imm(3, 20),
    mov_imm(1, 1),
    mov_imm(2, 1),
    mov_reg(4, 1),
    mov_reg(1, 2),
    mov_reg(2, 4),
    op_reg("add", 1, 1, 2),
    store(3, -1, 1),
    load(1, 0, 19), 
    branch("ltu", 1, 3, 3)]

prog_fact = [
    mov_imm(1, -20),
    mov_imm(2, -1),
    mov_imm(3, -1),  
    op_reg("mulhsu",4, 1, 2),
    op_reg("mul", 2, 2, 1),
    op_reg("mul", 3, 3, 1),
    op_reg("add", 3, 3, 4),
    op_imm("add", 1, 1, 1),
    branch("neq", 1, 0, 3)
]
print_prog(prog_fact)
print("\n"*130)