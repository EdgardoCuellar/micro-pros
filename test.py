# -*- coding: UTF-8 -*-

# c est un entier donnant le numéro du cycle
# p1 et p2 sont des listes de taille 5, donnant les numéros
#          des instructions dans chacun des étages des deux pipelines
# Reg est une liste de taille 10 donnant les contenus des registres
# Mem est une liste de taille 16 donnant les contenus des cases
#     mémoire

def printState(c, p1, p2, Reg, Mem):
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


def main():
    # Exemple d'utilisation

    # Mémoire: toutes les cases sont à 0 (valeur initiale)
    #          sauf la case d'adresse 3 qui contient 10
    M = [0 for x in range(16)]  # Mémoire
    M[3] = 10

    # Registres: tous les registres sont à 0 (valeur initiale)
    #            sauf le registre R2 qui contient 7
    R = [0 for x in range(10)]  # Registres
    R[2] = 7

    # Pipelines: le permier contient l'instruction 4 dans IF,
    #            l'instruction 2 dans ID et l'instruction 0 dans EX.
    #            Le second contient l'instruction 3 dans IF et la 1
    #            dans ID.
    #            Les autres étages sont vides
    p1 = [4, 2, 0, -1, -1]
    p2 = [3, 1, -1, -1, -1]

    printState(3, p1, p2, R, M)


main()
