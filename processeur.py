# -*- coding: utf-8 -*-
"""
Projet similateur de micro-processeur
Creation d'un processeur virtuel"ProcesseurZ8000" avec ses 10 registres et ces deux
pipelines et ses instructions.
Created on Tuesday November 27 14:31:11 2019
@author: Edgardo Cuellar Sanchez
N° de matricule : 496612
Mail : Edgardo.Cuellar.Sanchez@ulb.be
"""
import time

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

    :return:
    """
    rg = [0] * 10
    memories = [0] * 16
    pip = []
    for _ in range(2):
        pip.append([-1] * 5)
    with open(name) as prog_file:
        pr = prog_file.read().split("\n")
        return rg, memories, pip, pr


def printState(c, p1, p2, Reg, Mem):
    """

    :param c:
    :param p1:
    :param p2:
    :param Reg:
    :param Mem:
    :return:
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


def move(pip, deco, pr):
    """

    :param pip:
    :param deco:
    :param pr:
    :return:
    """
    for i in range(2):
        for j in range(4, 1, -1):
            if pip[i][j] != -1 and deco[pip[i][j]][j - 2] == 0:
                if j != 4:
                    pip[i][j + 1] = pip[i][j]
                pip[i][j] = -1
    for i in range(2):
        if pip[i][1] != -1:
            first_inst = list(set(pip[i]))
            where_pip = list(set(pip[0] + pip[1]))
            if set(pip[i][2:]) == {-1} and where_pip[0] == first_inst[0]:
                pip[i][2] = pip[i][1]
                pip[i][1] = -1
            elif where_pip[0] != first_inst[0]:
                if (pr[where_pip[0]].split(" ")[1] not in pr[pip[i][1]]
                        and pr[where_pip[0]].split(" ")[2] not in pr[pip[i][1]]):
                    pip[i][2] = pip[i][1]
                    pip[i][1] = -1
            elif pr[where_pip[0]].split(" ")[0] == "STORE" and pip[i][1] == where_pip[1] \
                    and (pip[0][-1] == where_pip[0] or pip[1][-1] == where_pip[0]):
                pip[i][2] = pip[i][1]
                pip[i][1] = -1

        if pip[i][0] != -1 and pip[i][1] == -1:
            pip[i][1] = pip[i][0]
            pip[i][0] = -1


def fetch(pip, pr, curs):
    """

    :param pip:
    :param pr:
    :param curs:
    :return:
    """
    for i in range(2):  # FETCH
        if curs < len(pr) - 1 and pip[i][0] == -1:
            pip[i][0] = curs
            curs += 1
    return curs


def decode(pip, pr, deco):
    """

    :param pip:
    :param pr:
    :param deco:
    :return:
    """
    for i in range(2):  # DECODE
        if pip[i][1] != -1:
            deco[pip[i][1]] = CYCLES[pr[pip[i][1]].split(" ")[0]][:]


def execute(rg, pip, pr, deco, v):
    """

    :param rg:
    :param pip:
    :param pr:
    :param deco:
    :param v:
    :return:
    """
    for i in range(2):  # EX
        if pip[i][2] in deco and deco[pip[i][2]][0] > 0:
            inst = pr[pip[i][2]].split(" ")
            if inst[0] == "IADD" or inst[0] == "IMUL":
                numbers = []
                for j in range(2):
                    numbers.append(rg[REGISTER_NAME.index(inst[j + 1])])
                if inst[0] == "IADD":
                    v[i] = 0
                    for nb in numbers:
                        v[i] += nb
                elif deco[pip[i][2]][0] == 3:
                    v[i] = 1
                    for nb in numbers:
                        v[i] *= nb
            deco[pip[i][2]][0] -= 1


def memory(rg, mem, pip, pr, deco, v):
    """

    :param v:
    :param rg:
    :param mem:
    :param pip:
    :param pr:
    :param deco:
    :return:
    """
    for i in range(2):  # MEM
        if pip[i][3] in deco and deco[pip[i][3]][1] > 0:
            inst = pr[pip[i][3]].split(" ")
            if inst[0] == "LOAD" and deco[pip[i][3]][1] == 2:
                v[i] = mem[int(inst[2])]
            elif inst[0] == "STORE":
                mem[int(inst[1])] = rg[REGISTER_NAME.index(inst[2])]
            deco[pip[i][3]][1] -= 1


def write_back(rg, pip, v, pr, deco):
    """

    :param rg:
    :param pip:
    :param v:
    :param pr:
    :param deco:
    :return:
    """
    for i in range(2):  # WB:
        if pip[i][4] in deco and deco[pip[i][4]][2] > 0:
            inst = pr[pip[i][4]].split(" ")
            if inst[0] != "STORE":
                if v[i] != "-1":
                    rg[REGISTER_NAME.index(inst[1])] = v[i]
                    v[i] = "-1"
                elif inst[0] == "MVC":
                    rg[REGISTER_NAME.index(inst[1])] = int(inst[2])
                else:
                    rg[REGISTER_NAME.index(inst[1])] = rg[REGISTER_NAME.index(inst[2])]
            deco[pip[i][-1]][-1] -= 1


def micro_pross(name):
    """

    :param name:
    :return:
    """
    registres, memoires, pipelines, prog = initialise(name)
    value = ["-1"] * 2
    first = True
    decoded = {}
    cursor_prog, count = 0, 1

    while set(pipelines[0]) != {-1} or set(pipelines[1]) != {-1} or first:
        first = False

        cursor_prog = fetch(pipelines, prog, cursor_prog)

        printState(count, pipelines[0], pipelines[1], registres, memoires)

        decode(pipelines, prog, decoded)

        execute(registres, pipelines, prog, decoded, value)

        memory(registres, memoires, pipelines, prog, decoded, value)

        write_back(registres, pipelines, value, prog, decoded)

        move(pipelines, decoded, prog)

        count += 1
    #  Print of the end
    printState(count, pipelines[0], pipelines[1], registres, memoires)


# main
if __name__ == '__main__':
    micro_pross(str(input("Name of the prog > ")))
