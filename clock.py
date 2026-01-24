################################################################################
######################             CLOCK          ##############################
################################################################################

from lib_carotte import *
from typing import *

from arith_unit import adder

def main():
    allow_ribbon_logic_operations(True)

    # compteur 8bit avec incrémentation à chaque cycle
    count = Reg(Defer(8, lambda: next_count))
    next_count, _ = adder(count, Constant("10000000"), Constant("0"))

    count.set_as_output("count")

# Exemple:
