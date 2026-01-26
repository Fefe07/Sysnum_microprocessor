# Sysnum_microprocessor
Ce projet contient la netlist correspondant à un microprocesseur.
La netlist a été obtenue en compilant du code python avec [Link text](https://github.com/CarottePy/carotte.py)

# Spécifications  
Adressage mémoire sur 32 bits  
Base ISA : RISC-V 32 bits  
Granularité mémoire : 1 octet, taille des mmots : 4 octest = 32 bits   
32 registres de 32 bits  
le code et la mémoire du processus partagent des espaces d'adressage séparés (architecture de Harvard)

Extensions possibles :
- [x] Multiplicateur
- [x] Pipelining
- [x] Bit shift


N.B. Write tests with gobbolt.org

# Compilation & Simulation
Une fois les bons chemins relatifs mis à jour (cf. plus bas) vous pouvez:
- compiler un circuit circuit.py avec :
`make circuit`
- lancer la simulation du dernier ciruit compilé avec :
`make sim`
- et donc si vous voulez compiler puis simuler circuit.py :
`make circuit sim`

Pour que cela fonctionne, il faut évidemment qu'il connaisse les chemins vers votre carotte.py et votre simulateur. 
Par défaut, les chemins sont correct si ces trois dossiers sont côte à côte.
- carotte.py
- Sysnum_microprocessor
- Netlist_simulator

avec le fichier carotte.py dans le dossier carotte.py et le fichier netlist_simulator.byte dans le dossier Netlist_simulator. 
Si ce n'est pas le cas, vous pouvez regarder le fichier config.mk et les mettre à jour. 

# Compilation de code assembleur pour le microprocesseur

Le fichier compiler.py permet de convertir du code assembleur ISA 32 bits en code machine pour le microprocesseur.  
Pour cela, il faut écrire le code dans un fichier, puis appeler la fonction python `compile` sur le chemin relatif du fichier, par exemple :  
```compile("compiler_test.ass")```
Le code produit est mis dans le fichier `compile.out`.  

Le code produit peut alors être éxécuté par le cpu, en le lançant avec `make cpu sim` puis en indiquant l'emplacement du code à éxécuter (ici `./compile.out`).  

# English
The netlist encoding of a microprocessor made in group for a digital systems course 