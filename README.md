# Sysnum_microprocessor
Ce projet contient la netlist correspondant à un microprocesseur.  
La netlist a été obtenue en compilant du code python avec [carotte.py](https://github.com/CarottePy/carotte.py).  
Ce projet a été effectué dans le cadre d'un cours de systèmes numériques à l'ENS Paris.

## Spécifications de base :
CPU RISC-V 32 bits 
Architecture Harvard : mémoire d'instructions et mémoire de données disjointes.
ISA RISC-V de base quasi complète avec extension M 
Toute adresse non alignée est tronquée ( modulo 4 octets )

## Compilation de code assembleur pour le microprocesseur

Le fichier compiler.py permet de convertir du code assembleur ISA 32 bits en code machine pour le microprocesseur.
Pour cela, il faut écrire le code dans un fichier, puis appeler la fonction python compile sur le chemin relatif du fichier, par exemple :
```compile("compiler_test.s")```  
Le code produit est mis dans le fichier compile.out.  

Le code produit peut alors être exécuté par le cpu, en le lançant avec `make cpu sim` puis en indiquant l'emplacement du code à exécuter (ici `./compile.out`).  

# Version de CPU avec pipeline
Compiler le circuit : make cpu pipeline
Créer un fichier assembleur .s avec seulement addi, add, lw, sw, qui est du type:
      addi x1, x0, 5
      addi x2, x0, 3
      add x3, x1, x2
      sw x3, x0, 0
Compiler: python3 compiler.py test.s
Simuler: python3 test_pipeline.py
Note: CPU_pipeline n'est pas compatible avec la clock et sa simulation passe par test_pipeline.py

## English
The netlist encoding of a microprocessor made in group for a digital systems course in ENS Paris.
