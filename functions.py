#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 07/03/2015
Ult. Modificacion el 07/03/2015

Este archivo define las funciones necesarias para la ejecucion del 
lenguaje Setlan.

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''

# OPERACIONES BINARIAS

# Suma para dos enteros
def suma(x,y):
    return x + y

# Resta para dos enteros
def resta(x,y):
    return x - y

# Multiplicacion de dos enteros
def multiplicacion(x,y):
    return x*y

# Division entera de dos enteros.
def division(x,y):
    return x//y

# Modulo de la division entera de dos enteros.
def modulo(x,y):
    return x%y

# And logico 
def logicAnd(x,y):
    return x and y

# Or Logico
def logicOr(x,y):
    return x or y

# Menor  para enteros
def menor(x,y):
    return x < y

# Mayor para enteros
def mayor(x,y):
    return x > y

# Menor o igual para enteros
def menorIgual(x,y):
    return x <= y

# Mayor o igual para enteros
def mayorIgual(x,y):
    return x >= y

# Igualdad para enteros, conjuntos y booleanos
def igual(x,y):
    return x == y

# Desigualdad para enteros, conjuntos y booleanos
def desigual(x,y):
    return x != y

# OPERACIONES PARA BINARIOS SOBRE CONJUNTOS
def setAListaDeEnteros(s):
    expreSet = str(s)
    elements = expreSet[1:-1].split(',')
    elements = map(int,elements)
    return elements

def listaDeEnterosASet(l):
    setString = "{"
    for item in l:
        setString += str(item) + ","
    setString = setString[:-1]
    setString += "}"
    return setString

# Retorna si un entero pertenece a un set determinado
def contiene(x,set):
    lista = setAListaDeEnteros(set)
    return x in lista