# Sysnum_microprocessor
Ce projet contient la netlist correspondant à un microprocesseur.  
La netlist a été obtenue en compilant du code python avec [carotte.py](https://github.com/CarottePy/carotte.py).  
Ce projet a été effectué dans le cadre d'un cours de systèmes numériques à l'ENS Paris.

## Spécifications  
Adressage mémoire sur 32 bits  
Base ISA : RISC-V 32 bits  
32 registres de 32 bits  
Le code et la mémoire du processus partagent des espaces d'adressage séparés (architecture de Harvard)

Extensions :
- Multiplicateur
- Diviseur

## Compilation & Simulation
Une fois les bons chemins relatifs mis à jour (cf. plus bas) vous pouvez:
- compiler un circuit circuit.py avec :
`make circuit`
- lancer la simulation du dernier ciruit compilé avec :
`make sim`
- et donc si vous voulez compiler puis simuler circuit.py :
`make circuit sim`

Pour que cela fonctionne, il faut que le microprocesseur connaisse les chemins vers carotte.py et vers le simulateur. 
Par défaut, les chemins sont correct si ces trois dossiers sont côte à côte :
- Sysnum_microprocessor
- carotte.py (https://github.com/CarottePy/carotte.py)
- Netlist_simulator (https://github.com/Acssiohm/Netlist_simulator),
(il faut que le fichier carotte.py soit dans le dossier carotte.py et le fichier netlist_simulator.byte dans le dossier Netlist_simulator -- si ce n'est pas le cas, vous pouvez regarder le fichier config.mk et les mettre à jour)

## Compilation de code assembleur pour le microprocesseur

Le fichier compiler.py permet de convertir du code assembleur ISA 32 bits en code machine pour le microprocesseur.
Pour cela, il faut écrire le code dans un fichier, puis appeler la fonction python compile sur le chemin relatif du fichier, par exemple :
```compile("compiler_test.s")```  
Le code produit est mis dans le fichier compile.out.  

Le code produit peut alors être exécuté par le cpu, en le lançant avec `make cpu sim` puis en indiquant l'emplacement du code à exécuter (ici `./compile.out`).  

# Version de CPU avec pipeline
Compiler le circuit : make cpu pipeline
Lancer la simulation : make sim pipelin
Quand le simulateur demande le fichier ROM, indiquer le chemin vers le programme compilé (ex : ./compile.out)
Par ailleurs, le CPU_pipeline n'est pas compatible avec la clock.

## English
The netlist encoding of a microprocessor made in group for a digital systems course in ENS Paris.
