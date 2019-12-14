# -*- coding: utf-8 -*-
"""
Projet similateur de micro-processeur
Creation d'un processeur virtuel"ProcesseurZ8000" avec ses 10 registres, 16 cases memoires
et deux pipelines (pipeline RISCclassique) qui permettent d'excecuter des instructions en
simultatné. Lit les instructions provenant d'un fichier txt qu'on lui donne, et excecute
les instructions.

Created on Tuesday December 11 16:42:37 2019
@author: Edgardo Cuellar Sanchez
N° de matricule : 496612
Mail : Edgardo.Cuellar.Sanchez@ulb.be
"""

# GLOBAL VARIABLE
REGISTER_NAME = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9"]
CYCLES = {"LOAD": [1, 2, 1],
          "STORE": [1, 1, 1],
          "MOVE": [1, 1, 1],
          "MVC": [1, 1, 1],
          "IADD": [1, 1, 1],
          "IMUL": [3, 1, 1]}


def initialise(name):
    """
    Simple fonction qui initialise les variables de base de notre processeur, telle que
    la memoire, les registres, les pipelines, et lit le fichier d'instruction
    :param name: le nom du fichier contenant les instructions
    :return: la memoire, les registres, les pipelines et les pipelines le tout initialisé
    """
    reg = [0] * 10  # Creation des registres
    memories = [0] * 16  # Creation de la mémoires
    pip = []
    for _ in range(2):  # Creation des deux pipelines
        pip.append([-1] * 5)
    with open(name) as prog_file:  # Lecture du fichier contenant le prog
        prog = prog_file.read().split("\n")
        return reg, memories, pip, prog


def printState(c, p1, p2, Reg, Mem):
    """
    Affiche simplement nos differentes parties de notre processeur, pour en connaitre
    l'avancement
    :param c: le cycle actuel de notre processeur
    :param p1: la pipeline 1
    :param p2: la pipeline 1
    :param Reg: les registres
    :param Mem: la memoire
    :return: None
    """
    print("Cycle:")
    print(c)
    print("Pipeline 1:")
    print(p1)
    print("Pipeline 2:")
    print(p2)
    print("Registres:")
    print(Reg)
    print("Memoire:")
    print(Mem)


def bloqued(pip, prog, i):
    """
    La fonction qui se charge de bloquer les instructions au bon moment, pour eviter des conflits
    entre les différentes instructions, le blocage s'effectuant à l'etage decode juste avant ex
    :param pip: un tableau contenant nos deux pipelines
    :param prog: les instructions du programme decoupé en tableau ligne par ligne
    :param i: pour savoir dans quelle pipelines nous nous trouvons
    :return: None
    """
    first_inst = list(set(pip[i]))
    where_pip = list(set(pip[0] + pip[1]))
    # Si il n'y a rien devant qui bloque avance simplement
    if set(pip[i][2:]) == {-1} and where_pip[0] == first_inst[0]:
        pip[i][2] = pip[i][1]
        pip[i][1] = -1
    # Si il y a des instructions cherche a savoire si il peut avancer ou non
    elif where_pip[0] != pip[i][1]:
        before_inst = where_pip[:where_pip.index(pip[i][1])]
        bloque = False
        for bif in before_inst:
            if prog[bif].split(" ")[1] in prog[pip[i][1]].split(" ")[1:] \
                    or prog[bif].split(" ")[2] in prog[pip[i][1]].split(" ")[1:]:
                bloque = True
        if not bloque:
            pip[i][2] = pip[i][1]
            pip[i][1] = -1
    # Si c'est un STORE il peut donc avancer si celui ci est à la dernière case
    elif prog[where_pip[0]].split(" ")[0] == "STORE" and pip[i][1] == where_pip[1] \
            and (pip[0][-1] == where_pip[0] or pip[1][-1] == where_pip[0]):
        pip[i][2] = pip[i][1]
        pip[i][1] = -1


def move(pip, deco, prog):
    """
    Deplace les instructions dans les pipelines dans l'ordre décroisant, et de manière a qu'il n'y
    est pas de conflit, ou de probleme.
    :param pip: un tableau contenant nos deux pipelines
    :param deco: les instructions decodé en dictionnaire
    :param prog: les instructions du programme decoupé en tableau ligne par ligne
    :return: None
    """
    for i in range(2):  # Fait avancer les 3 dernieres instructions dans l'ordre
        for j in range(4, 1, -1):
            if pip[i][j] != -1 and deco[pip[i][j]][j - 2] == 0:
                if j == 4:
                    pip[i][j] = -1
                elif pip[i][j + 1] == -1:
                    pip[i][j + 1] = pip[i][j]
                    pip[i][j] = -1
    for i in range(2):  # se charge de bloquer les instructions au bon moment pour eviter les bugs
        if pip[i][1] != -1:
            bloqued(pip, prog, i)

        if pip[i][0] != -1 and pip[i][1] == -1:
            pip[i][1] = pip[i][0]
            pip[i][0] = -1


def fetch(pip, prog, curs):
    """
    Va chercher la ligne de l'instruction et l'insere dans nos pipelines aux premieres case
    :param pip: un tableau contenant nos deux pipelines
    :param prog: les instructions du programme decoupé en tableau ligne par ligne
    :param curs: l'avancement dans les lignes de notre fichier programme
    :return: la ligne à la quelle nous somme dans le fichier
    """
    for i in range(2):  # FETCH
        if curs < len(prog) - 1 and pip[i][0] == -1:
            pip[i][0] = curs
            curs += 1
    return curs


def decode(pip, prog, deco):
    """
    Decode l'instruction grace a un tableau, et sait donc combien de cycle celle ci
    devra passer dans chacune des parties, tout cela dans un dictionnaire
    :param pip: un tableau contenant nos deux pipelines
    :param prog: les instructions du programme decoupé en tableau ligne par ligne
    :param deco: les instructions decodé en dictionnaire
    :return: None
    """
    for i in range(2):  # DECODE
        if pip[i][1] != -1:
            deco[pip[i][1]] = CYCLES[prog[pip[i][1]].split(" ")[0]][:]


def execute(reg, pip, prog, deco, var):
    """
    Execute l'instruction donné si il y a besoin de l'executé, certain cycle ne servant a rien
    et d'autres en prenant plusieurs, permet surtout les additions et les multiplication
    :param reg: un tableau contant tout les registres de notre processeur
    :param pip: un tableau contenant nos deux pipelines
    :param prog: les instructions du programme decoupé en tableau ligne par ligne
    :param deco: les instructions decodé en dictionnaire
    :param var: un dico de valeur en sorties des instructions, pour faciliter
    l'ecriture plus loin dans le processeur
    :return: None
    """
    for i in range(2):  # EX
        if pip[i][2] in deco and deco[pip[i][2]][0] > 0:
            inst = prog[pip[i][2]].split(" ")
            if inst[0] == "IADD" or inst[0] == "IMUL":
                numbers = []
                for j in range(2):
                    numbers.append(reg[REGISTER_NAME.index(inst[j + 1])])
                if inst[0] == "IADD":  # Effectue une simple addition en 1 cycle
                    var[pip[i][2]] = 0
                    for nb in numbers:
                        var[pip[i][2]] += nb
                elif deco[pip[i][2]][0] == 3:  # Effectue une simple multiplication en 1 cycle
                    var[pip[i][2]] = 1
                    for nb in numbers:
                        var[pip[i][2]] *= nb
            deco[pip[i][2]][0] -= 1


def memory(reg, mem, pip, prog, deco, var):
    """
    Gére la parties des instructions fesant appelle à la mémoires, écrit et lit les informations
    dans celle ci
    :param reg: un tableau contant tout les registres de notre processeur
    :param mem: un tableau contant tout la mémoire de notre processeur
    :param pip: un tableau contenant nos deux pipelines
    :param prog: les instructions du programme decoupé en tableau ligne par ligne
    :param deco: les instructions decodé en dictionnaire
    :param var: un dico de valeur en sorties des instructions, pour faciliter
    l'ecriture plus loin dans le processeur
    :return: None
    """
    for i in range(2):  # MEM
        if pip[i][3] in deco and deco[pip[i][3]][1] > 0:
            inst = prog[pip[i][3]].split(" ")
            if inst[0] == "LOAD" and deco[pip[i][3]][1] == 2:  # Lit la mémoire et stocke la donnée
                var[pip[i][3]] = mem[int(inst[2])]
            elif inst[0] == "STORE":  # Ecrit dans la mémoire depuis un registre
                mem[int(inst[1])] = reg[REGISTER_NAME.index(inst[2])]
            deco[pip[i][3]][1] -= 1


def write_back(reg, pip, var, prog, deco):
    """
    Gére les registres, permet d'ecrire les valeurs dans les registres
    :param reg: un tableau contant tout les registres de notre processeur
    :param pip: un tableau contenant nos deux pipelines
    :param var: un dico de valeur en sorties des instructions, pour faciliter
    l'ecriture plus loin dans le processeur
    :param prog: les instructions du programme decoupé en tableau ligne par ligne
    :param deco: les instructions decodé en dictionnaire
    :return: None
    """
    for i in range(2):  # WB:
        if pip[i][4] in deco and deco[pip[i][4]][2] > 0:
            inst = prog[pip[i][4]].split(" ")
            if inst[0] != "STORE":
                if pip[i][4] in var:  # Ecrit la valeur dans un registre
                    reg[REGISTER_NAME.index(inst[1])] = var[pip[i][4]]
                elif inst[0] == "MVC":  # Ecrit le nombre donnée dans la mémoire
                    reg[REGISTER_NAME.index(inst[1])] = int(inst[2])
                else:  # Copie un registre dans un autre
                    reg[REGISTER_NAME.index(inst[1])] = reg[REGISTER_NAME.index(inst[2])]
            deco[pip[i][-1]][-1] -= 1


def micro_pross(name):
    """
    La fonction principale de notre programme qui permet a tout le processeur de marcher
    en fesant appelle au différentre fonction de notre programme
    :param name: le nom du fichier contenant nos instructions
    :return: None
    """
    registres, memoires, pipelines, progra = initialise(name)
    value = {}
    decoded = {}
    cursor_prog, count = 0, 1

    while set(pipelines[0]) != {-1} or set(pipelines[1]) != {-1} or count == 1:

        cursor_prog = fetch(pipelines, progra, cursor_prog)  # IF

        printState(count, pipelines[0], pipelines[1], registres, memoires)  # Display

        decode(pipelines, progra, decoded)  # ID
        execute(registres, pipelines, progra, decoded, value)  # EX
        memory(registres, memoires, pipelines, progra, decoded, value)  # MEM
        write_back(registres, pipelines, value, progra, decoded)  # WB

        move(pipelines, decoded, progra)  # Move instruct

        count += 1
    #  Print of the end
    printState(count, pipelines[0], pipelines[1], registres, memoires)


# main
if __name__ == '__main__':
    micro_pross(str(input()))
