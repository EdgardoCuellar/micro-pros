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

def initialise():
    rg = [0]*10
    memories = [0]*16
    pip = []
    pr = []
    for _ in range(2):
        pip.append([-1]*5)
    with open(file_name) as prog_file:
        pr = prog_file.read().split("\n")
    return rg, memories, pip, pr


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


def move(pip, deco, prog):
    for i in range(2):
        for j in range(4, 1, -1):
            if j != 4 and pip[i][j] != -1 and decoded[pip[i][j]][j-2] == 0:
                pip[i][j+1] = pip[i][j]
            pip[i][j] = -1
        if pip[i][1] != -1:
            used = prog[pip[i][1]].split(" ")[1:]
            if set(pip[1][2:]) == {-1}:
                pip[i][2] = pip[i][1]
                pip[i][1] = -1
        if pip[i][0] != -1 and pip[i][1] == -1:
            pip[i][1] = pip[i][0]
            pip[i][0] = -1
    return pip


def fetch(pip, pr, curs):
    for i in range(2):  # FETCH
        if curs < len(pr) - 1 and pip[i][0] == -1:
            pip[i][0] = curs
            curs += 1
    return curs


def decode(pip, pr, deco):
    for j in range(2):  # DECODE
        if pip[j][1] != -1:
            deco[pip[j][1]] = CYCLES[pr[pip[j][1]].split(" ")[0]][:]


def execute(rg, pip, pr, deco, v):
    for j in range(2):  # EX
        if pip[j][2] in deco and deco[pip[j][2]][0] > 0:
            inst = pr[pip[j][2]].split(" ")
            numbers = (inst[1], inst[2])
            if inst[0] == "IADD":
                v[j] = 0
                for nb in numbers:
                    v[j] += rg[REGISTER_NAME.index(nb)]
            elif inst[0] == "IMUL" and deco[pip[j][2]][0] == 3:
                v[j] = 1
                for nb in numbers:
                    v[j] *= nb
            deco[pip[j][2]][0] -= 1


def memory(rg, mem, pip, pr, deco):
    for j in range(2):  # MEM
        if pip[j][3] in deco and deco[pip[j][3]][1] > 0:
            inst = pr[pip[j][3]].split(" ")
            if inst[0] == "LOAD" and deco[pip[j][3]][0] == 2:
                value[j] = mem[int(inst[2])]
            elif inst[0] == "STORE":
                mem[int(inst[1])] = rg[REGISTER_NAME.index(inst(2))]
            deco[pip[j][3]][1] -= 1


def write_back(rg, pip, v,  pr, deco):
    for j in range(2):  # WB:
        if pip[j][4] in deco and deco[pip[j][4]][2] > 0:
            inst = pr[pip[j][4]].split(" ")
            if inst[0] != "STORE":
                if v[j] != "-1":
                    rg[REGISTER_NAME.index(inst[1])] = v[j]
                    v[j] = "-1"
                else:
                    rg[REGISTER_NAME.index(inst[1])] = int(inst[2])
            deco[pip[j][-1]][-1] -= 1


if __name__ == '__main__':
    file_name = str(input("Name of the prog > "))

    registres, memoires, pipelines, prog = initialise()
    value = ["-1"]*2
    first = True
    decoded = {}
    cursor_prog, count = 0, 0

    while (set(pipelines[0]) != {-1} and set(pipelines[1]) != {-1}) or first:
        first = False

        cursor_prog = fetch(pipelines, prog, cursor_prog)

        count += 1
        printState(count, pipelines[0], pipelines[1], registres, memoires)

        decode(pipelines, prog, decoded)

        execute(registres, pipelines, prog, decoded, value)

        memory(registres, memoires, pipelines, prog, decoded)

        write_back(registres, pipelines, value, prog, decoded)

        print("- "*20)

        pipelines = move(pipelines, decoded, prog)

        time.sleep(0.5)
