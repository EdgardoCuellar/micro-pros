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
        pipelines.append([-1]*6)
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


def simulateur(reg, mem, pip, prog, count, where):
    for i in range(2):
        fetch(prog, pip, i, where)



def move(pip, what):
    pip.insert(0, what)
    pip.pop(len(pip)-1)
    return pip


def fetch(instruction, pip, who, where):
    pip[who] = instruction[where]
    where += 1


def decode(what):
    return CYCLES[what[0]]


def execute(i):
    pass


def memory(mem, where, what):
    if type(what) != int:
        return mem[where]
    else:
        mem[where] = what
        return mem[where]


def write_back(register, value, where):
    register[where] = value
    return register


if __name__ == '__main__':
    file_name = str(input("Name of the prog > "))

    registres, memoires, pipelines = initialise()
    prog = []
    decoded = []
    cursor_prog = 0
    count = 1
    with open(file_name) as prog_file:
        prog = prog_file.read().split("\n")

    while set(pipelines[0]) != {-1} and set(pipelines[1]) != {-1}:
        # simulateur(registres, memoires, pipelines, prog, count, cursor_prog)
        for i in range(2):
            if cursor_prog < len(prog):
                pipelines[i][0] = cursor_prog
                cursor_prog += 1
        count += 1
        for i in range(2):
            if pipelines[i][1] != -1:
                decoded.append(decode(prog[pipelines[i][1]]))


        printState(count, pipelines[0], pipelines[1], registres, memoires)
