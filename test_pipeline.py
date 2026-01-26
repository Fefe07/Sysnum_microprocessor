#pour tester la pipeline, mais ne marche qu'avec ces 4 instructions: addi add lw et sw
import sys

def decode(b):
    b = b[2:] if b.startswith('0b') else b
    op, rd, rs1, rs2 = b[25:32], int(b[20:25],2), int(b[12:17],2), int(b[7:12],2)
    imm = int(b[0:12],2) - (4096 if b[0]=='1' else 0)
    if op[2]=='1': return 'SW', 0, rs1, rs2, imm
    if op[3]=='1': return 'LW', rd, rs1, 0, imm
    if op[4]=='1': return 'ADDI', rd, rs1, 0, imm
    return 'ADD', rd, rs1, rs2, 0

def main(file):
    with open(file) as f:
        prog = [decode(l.strip()) for l in f if l.strip().startswith('0b')]
    
    pc, reg, mem = 0, [0]*32, [0]*64
    IF=ID=EX=MEM=None
    id_v1=id_v2=ex_res=ex_v2=ex_rd=ex_wen=wb_res=wb_rd=wb_wen=0
    
    for c in range(30):
        # Hazard?
        stall = EX and ID and EX[0]=='LW' and EX[1] and (EX[1]==ID[2] or EX[1]==ID[3])
        old = (ex_rd,ex_res,ex_wen,wb_rd,wb_res,wb_wen)
        
        # WB
        if MEM and wb_wen and wb_rd: reg[wb_rd] = wb_res
        
        # MEM
        MEM, wb_rd, wb_res, wb_wen = EX, old[0], old[1], old[2]
        if EX and EX[0]=='LW': wb_res = mem[ex_res//4]
        if EX and EX[0]=='SW': mem[ex_res//4] = ex_v2; wb_wen = 0
        
        # EX
        if stall:
            EX, ex_rd, ex_res, ex_v2, ex_wen = None, 0, 0, 0, 0
        elif ID:
            t,rd,r1,r2,imm = ID
            v1,v2 = id_v1, id_v2
            if r1 and r1==old[0] and old[2]: v1=old[1]
            elif r1 and r1==old[3] and old[5]: v1=old[4]
            if r2 and r2==old[0] and old[2]: v2=old[1]
            elif r2 and r2==old[3] and old[5]: v2=old[4]
            if t=='ADDI': ex_res=v1+imm
            elif t=='ADD': ex_res=v1+v2
            else: ex_res=v1+imm
            EX, ex_rd, ex_v2, ex_wen = ID, rd, v2, t in ['ADDI','ADD','LW']
        else:
            EX, ex_rd, ex_res, ex_v2, ex_wen = None, 0, 0, 0, 0
        
        # ID
        if not stall:
            ID = IF
            if IF: id_v1, id_v2 = reg[IF[2]], reg[IF[3]]
        
        # IF
        if not stall:
            IF = prog[pc//4] if pc//4 < len(prog) else None
            pc += 4
        
        def f(i): return f"{i[0]:4} x{i[1]},x{i[2]}" if i else "---"
        print(f"[{c+1:2}] IF:{f(IF):12} ID:{f(ID):12} EX:{f(EX):12} MEM:{f(MEM):12} | x1={reg[1]} x2={reg[2]} x3={reg[3]} m0={mem[0]}" + (" STALL" if stall else ""))
        
        if not any([IF,ID,EX,MEM]): break
    
    print(f"\n=> x1={reg[1]} x2={reg[2]} x3={reg[3]} mem[0]={mem[0]}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "compile.out")
