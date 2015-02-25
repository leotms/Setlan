#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 22/02/2015
Ult. Modificacion el 22/02/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''

# Funciones utiles:
# Retorna la identacion adecuada segun el vivel. 
def getIdent(level):
	return level * 4

# Imprime en pantalla con la identacion adecuada.
def printValueIdented(value, level):
	print getIdent(level)* " " + str(value)


# Un simbolo valido de la tabla. Cada simbolo tiene un nomre, tipo 
# y valor.
class Symbol(object):

	global symbol_default
	symbol_default = {
		'int' : 0,
		'bool': 'false',
		'set' : '{}'
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
		printValueIdented(string, level)

# Nodo de una tabla de simbolos. Contiene en un diccionario el simbolo,
# como su tipo y valor.
class SymbolNode(object):

    def __init__(self):
        self.symbols   = {}

    # Imprime todos los simbolos del nodo
    def printTable(self, level):
        for symbol in self.symbols:
           	self.symbols[symbol].printTable(level + 1)

    # Inserta un simbolo en el nodo
    def insert(self, variable, dataType):
        self.symbols[variable] = Simbolo(variable, dataType)

    # Elimina un simbolo del nodo
    def delete(self, variable):
            del self.symbols[variable]

# Tabla de Simbolos. Trata de seguir la estructura
# de una pila. 
class SymbolTable(object):

    def __init__(self, thisContext = None):

        #thisContext puede ser una tabla de simbolos u otro contexto.
        self.thisContext = thisContext
        self.nextContext = []

    #Imprime en pantalla el contexto.
    def printTable(self, level):
        if self.thisContext:
            printValueIdented("SCOPE",level)
            self.thisContext.printTable(level + 1)
            printValueIdented("END_SCOPE",level)
        if self.nextContext:
            self.nextContext.printTable(level + 1)

    def insert(self, variable, dataType):
        if not self.contains(variable):
            self.thisContext.insert(variable, dataType)
        else:
            return "Variable " + str(variable) + " already defined."
            #self.error(string)

    # def delete(self, variable):
    #     if self.contains(variable):
    #         del self.symbols[variable]
    #     else:
    #         string ="Variable '" + variable+ "' not defined."
    #         self.error(string)

    # def update(self, variable, dataType, value):
    #     if self.contains(variable):
    #         if variable in self.symbols:
    #             symbol = self.symbols[variable]

    #             if dataType == symbol.dataType:
    #                 symbol.value = value
    #                 self.symbols[variable] = symbol
    #                 return True
    #             else:
    #                 string = "SymTable.update: Different data types."
    #                 self.error.append(string)
    #                 return False
    #         else:
    #             return self.context.update(variable, dataType, value)
    #     else:
    #         print "SymTable.update: variable '" + variable + "' not defined."
    #         return False

    # Indica si una variable ya esta definida en el alcance mas
    # cercano del contesto.
    def contains(self, variable):
        # Solo se chequea el contexto mas cercano
        if isinstance(self.thisContext, SymbolNode):
            if variable in self.symbols:
                return True
        else:
            return False

    # def in_context(self, variable):
    #     if self.symbols:
    #         if variable in self.symbols:
    #             return True
    #     elif self.context:
    #         return self.context.in_context(variable)
    #     else:
    #         return False

    # def lookup(self, value):
    #     if self.symbols:
    #         if variable in self.symbols:
    #             return self.symbols[variable]
    #     elif self.context:
    #         return self.context.lookup(variable)
    #     return "Variable " + variable + " not in context."

    # def error(self, mensaje):
    #     self.errors.append(mensaje)