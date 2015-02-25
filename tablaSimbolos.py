#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 22/02/2015
Ult. Modificacion el 22/02/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''


# Funciones para la impresion
# Devuelve la identacion adecuada al nivel
def getIdent(level):
    return level * 4

# Imprime en pantalla un valor identado
def printValueIdented(value, level):
    print getIdent(level)* " " + str(value)

# Clase Simbolo
class Simbolo(object):

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

# Clase Tabla de Simbolos, provee lo necesario para construir una 
# nueva tabla de simbolos.
class tablaSimbolos(Table):
    pass

    def __init__(self):
        self.symbols  = {}
        self.parent   = None
        self.children = []
        # Comentado en caso de ser utilizado mas adelante.
        # self.errors  = []

    #Imprime los simbolos de la tabla actual y de sus sucesras.
    def printTable(self, level):
        # La tabla actual
        printValueIdented("SCOPE\n",level)
        for symbol in self.symbols:
            self.symbols[symbol].printTable(level + 1)
        printValueIdented("END_SCOPE\n",level)

        # Se imprimen los hijos
        if self.children:
            for child in clindren:
                child.printTable(level + 1children

    # def insert(self, variable, dataType):
    #     if not self.contains(variable):
    #         self.symbols[variable] = Simbolo(variable, dataType)
    #     else:
    #         string = "Variable " + str(variable) + " already in symbols"
    #         self.error(string)

    # def delete(self, variable):
    #     if self.contains(variable):
    #         del self.symbols[variable]
    #     else:
    #         string ="No '" + variable+ "' in symbols"
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
    #                 string = "SymTable.update: Different data types"
    #                 self.error.append(string)
    #                 return False
    #         else:
    #             return self.outer.update(variable, dataType, value)
    #     else:
    #         print "SymTable.update: No " + variable + " in symbols"
    #         return False

    # def contains(self, variable):
    #     if self.symbols:
    #         print(str(self.symbols))
    #         if variable in self.symbols:
    #             return True
    #     else:
    #         return False

    # def lookup(self, value):
    #     pass


    # def error(self, mensaje):
    #     self.errors.append(mensaje)

