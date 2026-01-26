#################################
#  Permet d'écrire des programmes en "pseudo-assembleur" 



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
        "sll" : 1, "sub" : 1,
        "and" : 2,
        "or"  : 3,
        "xor" : 4,
        "slt" : 5,
        "srl" : 6, "sra" : 6, 
        "sltu" : 7,

        "mul" : 0b000,
        "mulhsu" : 0b001,
        "mulhu": 0b010,
        "mulh" : 0b011,
        "div" : 0b111,
        "divu" : 0b110,
        "rem" : 0b101,
        "remu": 0b100
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

def get_opcode(jmp_kind, is_imm, read_from_ram = False, write_to_ram = False, is_type_u = False, is_auipc = False):
    ht_jmp = {
        "none": 0,
        "branch": 1,
        "jalr" : 2,
        "jal" : 3
    }
    return strb(is_auipc)+strb(is_type_u)+strb(write_to_ram)+strb(read_from_ram)+strb(is_imm)+get_number(ht_jmp[jmp_kind], 2, False)

def op_imm(op, dest, src, imm):
    imm_final = get_imm(imm, 12)
    if op in ["sll", "srl", "sra"] :
        imm_final = "0"+ strb(op == "sra") +"00000"+get_number(imm, 5, False)
    return get_instruction("i", imm_I = imm_final, rs1 = get_reg(src), rd = get_reg(dest), opcode = "0000100", funct3 = get_op(op))

def op_reg(op, dest, src1, src2):
    return get_instruction("r", rs2 = get_reg(src2), rs1 = get_reg(src1), rd = get_reg(dest), opcode = "0000000", funct7 = ("0000001" if op[:3] in ["mul", "div", "rem"] else ( "0100000" if op == "sub" or op == "sra" else "0000000" ) ), funct3 = get_op(op))

def branch(condition, src1, src2, addr):
    return get_instruction("b", 
    rs2 = get_reg(src2), 
    rs1 = get_reg(src1), 
    opcode = get_opcode("branch", False, False, False), 
    funct3 = get_condition(condition), 
    imm_B = get_imm(addr, 12))

def mov_imm(dest, imm):
    return op_imm("add", dest, 0, imm)

def mov_reg(dest, reg):
    return op_reg("add", dest, 0, reg)

def store(base, offset, src):
    return get_instruction("s", 
    imm_S = get_imm(offset, 12), 
    rs2 = get_reg(src), 
    rs1 = get_reg(base), 
    funct3 = "000", 
    opcode = get_opcode("none", True, False, True))

def load(dest, base, offset):
    return get_instruction("i", 
    imm_I = get_imm(offset, 12), 
    rs1 = get_reg(base), 
    rd = get_reg(dest), 
    funct3 = "000", 
    opcode = get_opcode("none", True, True, False) )

def jump(dest, offset):
    return get_instruction("j",
    imm_J = get_imm(offset, 20), 
    rd = get_reg(dest), 
    opcode = get_opcode("jal", True, False, False))

def jump_reg(dest, base, offset):
    return get_instruction("i", 
    imm_I = get_imm(offset, 12), 
    rd = get_reg(dest), 
    rs1 = get_reg(base), 
    funct3 = get_op("add"), 
    opcode = get_opcode("jalr", True, False, False, False, False))

def lui(dest, imm):
    return get_instruction("u", imm_U = get_imm(imm, 20), rd = get_reg(dest), opcode = get_opcode("none", True, False, False, True, False))

def auipc(dest, imm):
    return get_instruction("u", imm_U = get_imm(imm, 20), rd = get_reg(dest), opcode = get_opcode("none", True, False, False, True, True))

SP = 2
RA = 1

def call(offset):
    return jump(RA, offset)

def ret():
    return jump_reg(0, RA, 0)

def print_prog(p):
    print()
    need_pos = False
    for n,i in enumerate(p):
        if i != '0':
            if need_pos :
                print("."+str(4*n))
            print("0b"+i)
        else :
            need_pos = True
    print()