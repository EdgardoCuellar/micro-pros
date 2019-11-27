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

    initialise()

    with open(file_name) as prog_file:
        prog = prog_file.read().split("\n")
        for command in prog:
            commands = command.split(" ")
            if commands[0] == "LOAD":
                print(commands[1])

