#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 22/02/2015
Ult. Modificacion el 22/02/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''

from arbolST import *

class Table:

    def getIdent(self,level):
        return level * 4

    def printValueIdented(self, value, level):
        print self.getIdent(level)* " " + str(value)

class Simbolo(object):

    def __init__(self, nombre, tipo, valor = None):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor

    def printTable(self):
        if self.valor:
            valor = "| Value: " + str(self.valor)
        else
            valor = ""

        return "Variable: " + self.nombre + "| Type: " + self.tipo\
               + valor

class tablaSimbolos(Table):

    def __init__(self):
        self.scope = {}
        self.outer = None

    def printTable(self, level):
        self.printValueIdented("SCOPE\n",level)
        for symbol in self.scope:
            sym = self.scope[symbol]
            self.printValueIdented(sym.printTable(),level + 1)


    def insert(self, value):
        pass

    def delete(self, value):
        pass

    def update(self, value):
        pass

    def contains(self, value):
        pass

    def lookup(self, value):
        pass