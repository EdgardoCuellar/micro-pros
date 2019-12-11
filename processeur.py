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
    registres = [0]*10
    memories = [0]*16
    pipelines = []
    for _ in range(2):
        pipelines.append([-1]*5)
    return registres, memories, pipelines


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


def fetch(pip, what):
    pip[0] = what
    return pip


def decode(what):
    return CYCLES[what]


def execute(what, values, rg):
    if what:
        rp = 0
        for nb in values:
            rp += rg[REGISTER_NAME.index(nb)]
    else:
        rp = 1
        for nb in values:
            rp *= nb
    return rp


def memory(what, mem, rg, inst):
    if what:
        return mem[int(inst[2])]
    else:
        mem[int(inst[1])] = rg[REGISTER_NAME.index(inst(2))]
        return mem


def write_back(register, value, where):
    register[where] = value
    return register


if __name__ == '__main__':
    file_name = str(input("Name of the prog > "))

    registres, memoires, pipelines = initialise()
    pip_block = []
    prog = []
    value = ["-1"]*2
    first = True
    decoded = {}
    cursor_prog = 0
    count = 0
    with open(file_name) as prog_file:
        prog = prog_file.read().split("\n")

    while (set(pipelines[0]) != {-1} and set(pipelines[1]) != {-1}) or first:
        first = False
        # simulateur(registres, memoires, pipelines, prog, count, cursor_prog)

        for i in range(2):  # FETCH
            if cursor_prog < len(prog)-1 and pipelines[i][0] == -1:
                pipelines[i] = fetch(pipelines[i], cursor_prog)
                cursor_prog += 1

        count += 1
        printState(count, pipelines[0], pipelines[1], registres, memoires)

        for i in range(2):  # DECODE
            if pipelines[i][1] != -1:
                decoded[pipelines[i][1]] = decode(prog[pipelines[i][1]].split(" ")[0])

        for i in range(2):  # EX
            if pipelines[i][2] in decoded and decoded[pipelines[i][2]][0] > 0:
                instruct = prog[pipelines[i][2]].split(" ")
                if instruct[0] == "IADD":
                    value[i] = execute(True, (instruct[1], instruct[2]), registres)
                elif instruct[0] == "IMUL" and decoded[pipelines[i][2]][0] == 3:
                    value[i] = execute(False, (instruct[1], instruct[2]), registres)
                decoded[pipelines[i][2]][0] -= 1

        for i in range(2):  # MEM
            if pipelines[i][3] in decoded and decoded[pipelines[i][3]][1] > 0:
                instruct = prog[pipelines[i][3]].split(" ")
                if instruct[0] == "LOAD" and decoded[pipelines[i][3]][0] == 2:
                    value[i] = memory(True, memoires, registres, instruct)
                elif instruct[0] == "STORE":
                    memoires = memory(False, memoires, registres, instruct)
                decoded[pipelines[i][3]][1] -= 1

        for i in range(2):  # WB:
            if pipelines[i][4] in decoded and decoded[pipelines[i][4]][2] > 0:
                instruct = prog[pipelines[i][4]].split(" ")
                if instruct[0] != "STORE":
                    if value[i] != "-1":
                        registres[REGISTER_NAME.index(instruct[1])] = value[i]
                    else:
                        registres[REGISTER_NAME.index(instruct[1])] = int(instruct[2])
                    value[i] = "-1"
                decoded[pipelines[i][4]][2] -= 1

        print()

        pipelines = move(pipelines, decoded, prog)

        time.sleep(0.5)
