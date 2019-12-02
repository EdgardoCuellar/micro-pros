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


def simulateur(reg, mem, pip, prog, count):
    fetch(prog, pip)
    fetch(prog, pip)



def fetch(instruction, pip):
    if len(instruction) > 0:
        pip[0] = instruction[0]
        instruction.pop(0)


def decode(what):
    pass


def execute(i):
    pass


def memory(mem, what):
    pass


def write_back(register, memory, prog):
    pass


if __name__ == '__main__':
    file_name = str(input("Name of the prog > "))

    registres, memoires, pipelines = initialise()
    prog = []
    count = 1
    with open(file_name) as prog_file:
        prog = prog_file.read().split("\n")

    while set(pipelines[0]) != {-1} and set(pipelines[1]) != {-1}:
        simulateur(registres, memoires, pipelines, prog, count)
        printState(count, pipelines[0], pipelines[1], registres, memoires)
        count += 1
