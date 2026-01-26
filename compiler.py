##########################
# Compiler assembly to code
#######################


# TODO : push, pop, call, ret, register aliases(done)


from instructions import *
from log_unit import clone

def print_prog_file(p, f):
    # Imprime le programme construit p dans le fichier de sortie f
    need_pos = False
    for n,i in enumerate(p):
        if i != '0':
            if need_pos :
                f.write("."+str(4*n)+"\n")
            f.write("0b"+i+"\n")
        else :
            need_pos = True
    f.write("\n")

def get_line_words(file_in) :
    # Renvoie la prochaine ligne non blanche et la liste de ses mots, sans virgule

    words = []

    # élimination des lignes blanches
    while words == [] : 
        line = file_in.readline()
        while line == "" :
            line = file_in.readline()
            if not line :
                return None, None

        if line[-1]=='\n' :
            line = line[:len(line)-1]
        line = line.replace(',', ' ')
        #print(line)
        words = line.split(' ')
        while '' in words :
            words.remove('')
    

    for i in range(1,len(words)) :
    #gestion des alias 
        words[i] = words[i].replace('zero', 'x0')
        words[i] = words[i].replace('ra', 'x1')
        words[i] = words[i].replace('sp', 'x2')
        words[i] = words[i].replace('gp', 'x3')
        words[i] = words[i].replace('tp', 'x4')
        words[i] = words[i].replace('t0', 'x5')
        words[i] = words[i].replace('t1', 'x6')
        words[i] = words[i].replace('t2', 'x7')
        words[i] = words[i].replace('s0', 'x8')
        words[i] = words[i].replace('fp', 'x8')
        words[i] = words[i].replace('s1', 'x9')
        words[i] = words[i].replace('a0', 'x10')
        words[i] = words[i].replace('a1', 'x11')
        words[i] = words[i].replace('a2', 'x12')
        words[i] = words[i].replace('a3', 'x13')
        words[i] = words[i].replace('a4', 'x14')
        words[i] = words[i].replace('a5', 'x15')
        words[i] = words[i].replace('a6', 'x16')
        words[i] = words[i].replace('a7', 'x17')
        words[i] = words[i].replace('s2', 'x18')
        words[i] = words[i].replace('s3', 'x19')
        words[i] = words[i].replace('s4', 'x20')
        words[i] = words[i].replace('s5', 'x21')
        words[i] = words[i].replace('s6', 'x22')
        words[i] = words[i].replace('s7', 'x23')
        words[i] = words[i].replace('s8', 'x24')
        words[i] = words[i].replace('s9', 'x25')
        words[i] = words[i].replace('s10', 'x26')
        words[i] = words[i].replace('s11', 'x27')
        words[i] = words[i].replace('t3', 'x28')
        words[i] = words[i].replace('t4', 'x29')
        words[i] = words[i].replace('t5', 'x30')
        words[i] = words[i].replace('t6', 'x31')

    #print(line)
    return line, words
    
def get_val_from_label(label, labels, labels_num, n) :
    # Permet de calculer le décalage relatif à partir du label
    # Gros calculs à cause de la fonctionnalité 1b/1f

    if int(label[0]) in list(range(1,10)):
        if len(label)!=2 :
            print("Syntaxes autorisées pour labels commençant par un chiffre (i) : if et ib")
        assert(len(label)==2)
        k = int(label[0])-1
        if label[1] == "f" :
            i = 0 
            while i < len(labels_num[k]) and labels_num[k][i] <= n :
                i += 1
            if i == len(labels_num[k]):
                print("pas de label ", k, " après")
                assert(False)
            else :
                val = 4*(labels_num[k][i] - n)
        elif label[1] == "b" :
            i = len(labels_num[k])-1 
            while i >=0 and labels_num[k][i] > n :
                print("n = ", n)
                print("labels_num[k][i] = ", labels_num[k][i])
                i -= 1
            if i == -1:
                print("pas de label ", k, " avant")
                assert(False)
            else :
                val = 4*(labels_num[k][i] - n)
        else :
            print("Syntaxes autorisées pour labels commençant par un chiffre (i) : if et ib")
            assert(False)


    else :
        val = 4*(labels[label] - n)
    return val


def compile(filename) :

    ## Premier passage pour repérer les labels

    labels = {}
    labels_num = 9*[[]]

    program = []
    file_in = open(filename, "r")
    line,words = get_line_words(file_in)

    # n compte les lignes de code produit
    n = 0
    while line :
        #words = get_line_words(file_in)
        if words[0][-1] == ':' :
            name = words[0][:-1]
            # if name[-1]==':' :
            #     name = name[:len(name)-1]
            if int(name) in list(range(1,10)) :
                labels_num[int(name)-1].append(n)
            else :
                labels[name]= n 
        else :
            # n compte uniquement les lignes de code produit
            n += 1

        line,words = get_line_words(file_in)
    file_in.close()
    # print("labels :")
    # print(labels)
    # print("labels_num :")
    # print(labels_num)


    ## Second passge : construction du programme 

    program = []
    file_in = open(filename, "r")
    file_out = open("compile.out", "w")
    # n compte les lignes de code produit
    n = 0

    line,words = get_line_words(file_in)

    while line != None :

        if len(words)>=2 :
            if words[1][0] == "x" :
                #registres
                #print("words[1][2:] = ", words[1][2:])
                val_1 = int(words[1][1:])
                is_cst_1 = False
            
            elif words[1][0] == '"' :
                # labels
                val_1 = get_val_from_label(words[1][1:-1], labels, labels_num, n)
                is_cst_1 = True

            else :
                val_1 = int(words[1])
                is_cst_1 = True
            #print("val_1 = ", val_1)

            if len(words) >= 3 :

                if words[2][0] == "x" :
                    val_2 = int(words[2][1:])
                    is_cst_2 = False
                elif words[2][0] == '"' :
                    # labels
                    val_2 =  get_val_from_label(words[2][1:-1], labels, labels_num, n)
                    is_cst_2 = True
                else :
                    val_2 = int(words[2])
                    is_cst_2 = True
                # print("val_2 = ", val_2)

                if len(words) == 4 :
                    assert(not is_cst_2)
                    if words[3][0] == "x" :
                        val_3 = int(words[3][1:])
                        is_cst_3 = False
                    elif words[3][0] == '"' :
                        # labels
                        val_3 = get_val_from_label(words[3][1:-1], labels, labels_num, n)
                        is_cst_3 = True
                    else :
                        val_3 = int(words[3])
                        is_cst_3 = True
                    #print("val_3 = ", val_3)

                    #print(is_cst_3)
                    match (words[0],is_cst_3) :
                        
                        case ("addi",True) :
                            program.append(op_imm("add",val_1 ,val_2 ,val_3 ))
                        case ("add", False) :
                            program.append(op_reg("add",val_1 ,val_2 ,val_3 ))
                        case ("sub", False) :
                            program.append(op_reg("sub",val_1 ,val_2 ,val_3 ))
                        case ("mul", False) :
                            program.append(op_reg("mul", val_1, val_2, val_3))
                        case ("mulh", False) :
                            program.append(op_reg("mulh", val_1, val_2, val_3))
                        case ("mulhu", False) :
                            program.append(op_reg("mulhu", val_1, val_2, val_3))
                        case ("mulhsu", False) :
                            program.append(op_reg("mulhsu", val_1, val_2, val_3))
                        case ("sll", False) :
                            program.append(op_reg("sll",val_1 ,val_2 ,val_3 ))
                        case ("slli", True) :
                            program.append(op_imm("sll",val_1 ,val_2 ,val_3 ))
                        case ("srl", False) :
                            program.append(op_reg("srl",val_1 ,val_2 ,val_3 ))
                        case ("srli", True) :
                            program.append(op_imm("srl",val_1 ,val_2 ,val_3 ))
                        case ("sra", False) :
                            program.append(op_reg("sra",val_1 ,val_2 ,val_3 ))
                        case ("srai", True) :
                            program.append(op_imm("sra",val_1 ,val_2 ,val_3 ))
                        case ("and", False) :
                            program.append(op_reg("and",val_1 ,val_2 ,val_3 ))
                        case ("andi", True) :
                            program.append(op_imm("and",val_1 ,val_2 ,val_3 ))
                        case ("or", False) :
                            program.append(op_reg("or",val_1 ,val_2 ,val_3 ))
                        case ("ori", True) :
                            program.append(op_imm("or",val_1 ,val_2 ,val_3 ))
                        case ("xor", False) :
                            program.append(op_reg("xor",val_1 ,val_2 ,val_3 ))
                        case ("xori", True) :
                            program.append(op_imm("xor",val_1 ,val_2 ,val_3 ))
                        case ("slt", False) :
                            program.append(op_reg("slt",val_1 ,val_2 ,val_3 ))
                        case ("slti", True) :
                            program.append(op_imm("slt",val_1 ,val_2 ,val_3 ))
                        case ("sltu", False) :
                            program.append(op_reg("sltu",val_1 ,val_2 ,val_3 ))
                        case ("sltui", True) :
                            program.append(op_imm("sltu",val_1 ,val_2 ,val_3 ))
                        case ("beq", _) :
                            program.append(branch("eq", val_1, val_2, val_3))
                        case ("bne", _) :
                            program.append(branch("neq", val_1, val_2, val_3))
                        case ("blt", _) :
                            program.append(branch("lt", val_1, val_2, val_3))
                        case ("bgt", _) :
                            program.append(branch("lt", val_2, val_1, val_3))
                        case ("bge", _) :
                            program.append(branch("ge", val_1, val_2, val_3))
                        case ("ble", _) :
                            program.append(branch("ge", val_2, val_1, val_3))
                        case ("bltu", _) :
                            program.append(branch("ltu", val_1, val_2, val_3))
                        case ("bgtu", _) :
                            program.append(branch("ltu", val_2, val_1, val_3))
                        case ("bgeu", _) :
                            program.append(branch("geu", val_1, val_2, val_3))
                        case ("bleu", _) :
                            program.append(branch("geu", val_2 val_1, val_3))
                        case ("jalr", True) :
                            program.append(jump_reg(val_1, val_2, val_3))
                        case ("lw", True) :
                            # destination puis source puis offset
                            program.append(load(val_1, val_2, val_3))
                        #lb, lbu, lh, lhu plus compliqués car il faut modifier le mot chargé 

                        # case ("lbu", True) :
                        #     # destination puis source puis offset
                        #     program.append(load(val_1, val_2, val_3))
                        #     program.append(mov_reg(val_1, val_1))
                        case ("sw", True) :
                            program.append(store(val_2, val_3, val_1))
   
                        case _ :
                            print("Opération non traitée")
                            print("Peut-être avez vous utilisé un mot-clé pour immédiat et donné un registre ou inversement ?")
                            assert(False)
                            


                else :
                    assert(len(words) == 3)
                    match words[0], is_cst_2 :
                        case ("jal", True) :
                            program.append(jump(val_1, val_2))
                        case("lui", True) :
                            program.append(lui(val_1, val_2))
                        case("auipc", True) :
                            program.append(auipc(val_1, val_2))
                        case("mov", True) :
                            program.append(mov_imm(val_1, val_2))
                        case("mov", False) :
                            program.append(mov_reg(val_1, val_2))
                        case("jr", True) :
                            program.append(jump_reg(0, val_1, val_2))
                        case _ : 
                            print("Opération non traitée")
                            assert(False)

            elif len(words) == 2 :
                match words[0], is_cst_1 :
                    case ("call", True) :
                        program.append(call(val_1))
                    case("pop", False) :
                        program.append(pop(val_1))
                    case("push", False) :
                        program.append(push(val_1))
                    case("j", True) :
                        program.append(jump(0,val_1))


            else :
                assert(False)
        else :
            match words[0] :
                case("ret") :
                    program.append(ret())
            
            
        if words[0][-1] != ":" :
            # n compte uniquement les lignes de code produit
            n+=1
        

        line, words = get_line_words(file_in)

    print_prog(program)
    print_prog_file(program,file_out)

    #print("Fin du fichier")

    file_in.close()

# Modifier cette ligne pour compiler un autre code
compile("clock.s")





