#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 22/02/2015
Ult. Modificacion el 22/02/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''


class Simbolo(object):

	def __init__(self, nombre, tipo, valor = None):
		self.nombre = nombre
		self.tipo = tipo
		self.valor = valor

	def __str__(self):
		if self.valor:
			valor = "| Value: " + str(self.valor)
		else
			valor = ""

		return "Variable: " + self.nombre + "| Type: " + self.tipo\
		       + valor