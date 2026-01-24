################################################################################
######################         HAZARD           ################################
################################################################################
#si hazard alors le pipeline doit etre "stall" ou "flush"
#https://en.wikipedia.org/wiki/Pipeline_stall
#https://en.wikipedia.org/wiki/Hazard_(computer_architecture)#PIPELINE-FLUSH
from lib_carotte import *
from typing import *

from log_unit import b_or, b_and

# détecte quand un LOAD est en EX et qu'il est suivi d'une instruction qui doit 
# utiliser le résultat juste après
def hazard_detection(id_rs1, id_rs2, ex_rd, ex_read_from_ram):
    # si stall -> insérer une bulle (NOP) entre ID et EX, bloquer IF et ID
    allow_ribbon_logic_operations(True)
    
    rs1_eq_ex_rd = ~b_or(id_rs1 ^ ex_rd)
    rs2_eq_ex_rd = ~b_or(id_rs2 ^ ex_rd)
    
    ex_rd_not_zero = b_or(ex_rd) # ex_rd != x0
    
    # Load-use hazard : EX fait un LOAD et ID a besoin du résultat
    stall = ex_read_from_ram & ex_rd_not_zero & (rs1_eq_ex_rd | rs2_eq_ex_rd)
    
    return stall


def flush_test(branch_taken, jump):
    flush = branch_taken | jump
    return flush

def main():
    allow_ribbon_logic_operations(True)

    id_rs1 = Input(5)
    id_rs2 = Input(5)
    ex_rd = Input(5)
    ex_load = Input(1)
    
    stall = hazard_detection(id_rs1, id_rs2, ex_rd, ex_load)
    stall.set_as_output("stall")
    
    branch = Input(1)
    jump = Input(1)
    flush = flush_test(branch, jump)
    flush.set_as_output("flush")

# Exemple:
# Step 1 : 
# id_rs1 ? 0b00001
# id_rs2 ? 0b00010
# ex_rd  ? 0b00011
# ex_load? 0b0
# branch ? 0b0
# jump   ? 0b0
# => stall = 0
# => flush = 0
#
# Step 2 :
# id_rs1 ? 0b00101
# id_rs2 ? 0b00010
# ex_rd  ? 0b00101
# ex_load? 0b1
# branch ? 0b0
# jump   ? 0b0
# => stall = 1
# => flush = 0
#
# Step 3 :
# id_rs1 ? 0b00001
# id_rs2 ? 0b00010
# ex_rd  ? 0b00011
# ex_load? 0b0
# branch ? 0b1
# jump   ? 0b0
# => stall = 0
# => flush = 1
