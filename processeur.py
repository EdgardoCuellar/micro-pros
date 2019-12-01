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


class PipeLine:

    def __init__(self, size):
        self.size = size

    def if_instruct(self):
        pass

    def id_instruct(self):
        pass

    def ex_instruct(self):
        pass

    def mem_instruct(self):
        pass

    def wb_instruct(self):
        pass


class Registre:

    def __init__(self, who, value):
        self.who = who
        self.value = value


class Memorie:

    def __init__(self, who, value):
        self.who = who
        self.value = value


def initialise():
    registres = []
    memorie = []
    for i in range(10):
        registres.append(Registre(i, 0))
    for i in range(16):
        memorie.append(Memorie(i, 0))
    return registres, memorie


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


def load():
    pass


def store():
    pass


def move():
    pass


def mvc():
    pass


def iadd():
    pass


def imul():
    pass


if __name__ == '__main__':
    file_name = str(input("Name of the prog > "))

    registres, memoires = initialise()

    with open(file_name) as prog_file:
        prog = prog_file.read().split("\n")
        for c in range(0, len(prog), 2):
            commands = prog[c].split(" ")
            print(commands)
            if commands[0] == "LOAD":
                load()
                # print(commands[1])
            elif commands[0] == "STORE":
                store()
            elif commands[0] == "MOVE":
                move()
            elif commands[0] == "MVC":
                mvc()
            elif commands[0] == "IADD":
                iadd()
            elif commands[0] == "IMUL":
                imul()


