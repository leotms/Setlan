#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 22/02/2015
Ult. Modificacion el 22/02/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''


class Simbolo(object):

	global symbol_default
	symbol_default = {
		'INT' : 0,
		'BOOL': 'false',
		'SET' : '{}'
	}

	def __init__(self, name, type, value = None):
		self.name = name
		self.type = type
		# Colocamos el valor por defecto
		if value == None:
			self.value = symbol_default[type]
		else:
			self.value = value

	def printTable(self, level):
		string  = "Variable: " + self.name
		string += " | Type: "   + self.type
		string += " | Value: " + str(self.value)
		self.printValueIdented(string, level)

class tablaSimbolos(Table):

    def __init__(self):
        self.actual   = {}
        self.children = []
        self.parent   = None
        self.errors   = []

    def printTable(self, level):
        self.printValueIdented("SCOPE\n",level)
        if self.children:
        	for child in self.children:
        		child.printTable(level+1)
        else:
        	for symbol in self.actual:
            	self.actual[symbol].printTable(level + 1)
        self.printValueIdented("END_SCOPE\n",level)


    def insert(self, variable, dataType):
        if not self.contains(variable):
            self.actual[variable] = Simbolo(variable, dataType)
        else:
            string = "Variable " + str(variable) + " already defined."
            self.error(string)

    def delete(self, variable):
        if self.contains(variable):
            del self.actual[variable]
        else:
            string ="Variable '" + variable+ "' not defined."
            self.error(string)

    def update(self, variable, dataType, value):
        if self.contains(variable):
            if variable in self.actual:
                symbol = self.actual[variable]

                if dataType == symbol.dataType:
                    symbol.value = value
                    self.actual[variable] = symbol
                    return True
                else:
                    string = "SymTable.update: Different data types."
                    self.error.append(string)
                    return False
            else:
                return self.parent.update(variable, dataType, value)
        else:
            print "SymTable.update: variable '" + variable + "' not defined."
            return False

    def contains(self, variable):
        if self.actual:
            if variable in self.actual:
                return True
        else:
            return False

    def inContext(self, variable):
    	if self.actual:
    		if variable in self.actual:
    			return True
    	else if self.parent:
    		return self.parent.inContext(variable)
    	else:
    		return False

    def lookup(self, value):
    	if self.actual:
    		if variable in self.actual:
    			return self.actual[variable]
    	else if self.parent:
    		return self.parent.lookup(variable)
    	return "Variable " + variable + " not in context."

    def error(self, mensaje):
        self.errors.append(mensaje)
