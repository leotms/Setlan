#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 22/02/2015
Ult. Modificacion el 22/02/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''

def scope(target, scope):
    if isinstance(target, Block):
        target.symTable.outer = scope
    else:
        target.symTable = scope

class Table:

    def getIdent(self,level):
        return level * 4

    def printValueIdented(self, value, level):
        print self.getIdent(level)* " " + str(value)


class Simbolo(Table):

    def __init__(self, name, dataType, value = None):
        self.name = name
        self.type = dataType
        self.value = value

    def printTable(self, level):
        if self.valor:
            valor = "| Value: " + str(self.valor)
        else:
            valor = ""

        string  = "Variable: " + self.name + "| Type: " + self.tipo
        string += valor
        self.printValueIdented(string, level)

class tablaSimbolos(Table):

    def __init__(self):
        self.scope = {}
        self.outer = None

    def printTable(self, level):
        self.printValueIdented("SCOPE\n",level)
        for symbol in self.scope:
            sym.printTable(level + 1)
        self.printValueIdented("END_SCOPE\n",level)


    def insert(self, variable, dataType):
        if not self.contains(variable):
            self.scope[variable] = Simbolo(variable, dataType)
        else:
            return "Variable " + variable + " already in scope"

    def delete(self, variable):
        if self.contains(variable):
            del self.scope[variable]
        else:
            print "No '" + variable+ "' in scope"

    def update(self, variable, dataType, value):
        if self.contains(variable):
            if variable in self.scope:
                symbol = self.scope[variable]

                if dataType == symbol.dataType:
                    symbol.value = value
                    self.scope[variable] = symbol
                    return True
                else:
                    print "SymTable.update: Different data types"
                    return False
            else:
                return self.outer.update(variable, dataType, value)
        else:
            print "SymTable.update: No " + variable + " in scope"
            return False

    def contains(self, variable):
        if self.scope:
            return (variable in self.scope)

    def lookup(self, value):
        pass

