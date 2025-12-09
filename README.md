# Sysnum_microprocessor
The netlist encoding of a microprocessor made in group for a digital systems course  

Adressage mémoire sur 32 bits  
Base ISA : RISC-V 32 bits  
Granularité mémoire : 1 octet   
32 registres de 32 bits  
le code et la mémoire du processus partagent des espaces d'adressage séparés (architecture de Harvard)

Extensions possibles :
- Multiplicateur
- Pipelining
- Bit shift
N.B. Write tests with gobbolt.org
