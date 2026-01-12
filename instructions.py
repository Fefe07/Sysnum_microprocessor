def get_instruction(t, **args):
    if t == "r" :
        res = args["funct7"]+args["rs2"]+args["rs1"]+args["funct3"]+args["rd"]+args["opcode"]
    elif t == "i":
        res = args["imm_I"]+args["rs1"]+args["funct3"]+args["rd"]+args["opcode"]
    elif t == "s":
        res = args["imm_S"][0:-5]+args["rs2"]+args["rs1"]+args["funct3"]+args["imm_S"][-5:0]+args["opcode"]
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
        "xor" : 5
    }
    return get_number(ht[op], 3, False)

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

def op_imm(op, dest, src, imm):
    return get_instruction("i", imm_I = get_number(imm, 12, True), rs1 = get_number(src, 5, False), rd = get_number(dest, 5, False), opcode = "0000100", funct3 = get_op(op))

def op_reg(op, dest, src1, src2):
    return get_instruction("r", rs2 = get_number(src2, 5, False), rs1 = get_number(src1, 5, False), rd = get_number(dest, 5, False), opcode = "0000000", funct7 = "0000000", funct3 = get_op(op))

def branch(condition, src1, src2, addr):
    return get_instruction("b", rs2 = get_number(src2, 5, False), rs1 = get_number(src1, 5, False), opcode = "0000010", funct3 = get_condition(condition), imm_B = get_number(addr, 12, True))

def mov_imm(dest, imm):
    return op_imm("add", dest, 0, imm)

def mov_reg(dest, reg):
    return op_reg("add", dest, 0, reg)

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