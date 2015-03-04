#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 05/02/2015
Ult. Modificacion el 09/02/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''


#Importamos
from tablaSimbolos import *
from   lexer       import find_column

#Errores
type_error_list = []

#Empila una nueva tabla de simbolos
def empilar(objeto, alcance):
    if isinstance(objeto, Block):
        objeto.alcance.parent = alcance
        alcance.children.append(objeto.alcance)
    else:
        objeto.alcance = alcance

# Clase Expression.
class Expression:
    pass

#Siempre es el primer elemento de un codigo setlan. 
class Program(Expression):

    def __init__(self, statement):
        self.type      = "PROGRAM"
        self.statement = statement
        self.alcance   = tablaSimbolos()

    def printTree(self, level):
        printValueIdented(self.type, level)
        self.statement.printTree(level+1)

    def symbolcheck(self):
        empilar(self.statement, self.alcance)
        if self.statement.symbolcheck():
            return self.alcance

#Clase para la asignacion de expresiones
class Assign(Expression):

    def __init__(self, leftIdent, rightExp):
        self.type      = "ASSIGN"
        self.leftIdent = leftIdent
        self.rightExp  = rightExp

    def printTree(self,level):
        printValueIdented(self.type, level)
        #Impresion del identificador asignado
        printValueIdented("IDENTIFIER", level + 1)
        self.leftIdent.printTree(level + 2)
        #Impresion de la expresion asignada
        printValueIdented("VALUE", level + 1)
        self.rightExp.printTree(level + 2)

    def symbolcheck(self):
        empilar(self.rightExp, self.alcance)
        empilar(self.leftIdent, self.alcance)
    
        #Buscamos los tipos
        RightExpType  = self.rightExp.symbolcheck()
        LeftIdentType = self.leftIdent.symbolcheck()

        if LeftIdentType and RightExpType:
            #Verificamos que la asignacion cumpla el tipo del identificador
            if LeftIdentType != RightExpType: 
                mensaje  = "ERROR: No se puede asignar '" + RightExpType \
                           + "' a Variable '" + str(self.leftIdent) + "' de tipo '"\
                           + str(LeftIdentType) + "'"
                type_error_list.append(mensaje)

        if LeftIdentType:
            identifier = self.alcance.buscar(self.leftIdent.identifier)
            if not identifier.modifiable:
                mensaje = "ERROR: No se puede modificar " + self.leftIdent
                type_error_list.append(mensaje)

# Clase para la impresion por consola
class Print(Expression):
 
    def __init__(self, printType, elements):
        self.type     = printType
        self.elements = elements
 
    def printTree(self, level):
        printValueIdented(self.type,level)
        for element in self.elements:
            element.printTree(level + 1)

    def symbolcheck(self):
        
        accepted_types = ['string','int','bool','set']
        for element in self.elements:
            empilar(element, self.alcance)
            elemtype = element.symbolcheck()
    
            #Verificamos que se impriman expresiones de tipos permitidos
            if not elemtype in accepted_types:
                mensaje =  "ERROR: No se puede imprimir '"\
                           + elemtype + "'."
                type_error_list.append(mensaje)

# Clase para la entrada de datos
class Scan(Expression):
    
    def __init__(self, identifier):
        self.type  = 'SCAN'
        self.value = identifier

    def printTree(self,level):
        printValueIdented(self.type,level)
        self.value.printTree(level + 1)

    def symbolcheck(self):
        accepted_types = ['int','bool']
        empilar(self.value, self.alcance)
        valueType = self.value.symbolcheck()

        #Verificamos que se admita el tipo permitido
        if not valueType in accepted_types:
            mensaje = "ERROR: scan no admite valores de tipo '"\
                      + valueType + "'."   
            type_error_list.append(mensaje) 

#Un bloque es una secuencia de Expresiones
class Block(Expression):
  
    def __init__(self, list_inst, declaraciones = None):
        self.type          = "BLOCK"
        self.list_inst     = list_inst
        self.declaraciones = declaraciones
        self.alcance       = tablaSimbolos()
  
    def printTree(self,level):
        printValueIdented(self.type,level)
        
        #Imprimimos la lista de declaraciones, si existe
        if self.declaraciones:
            self.declaraciones.printTree(level+1)
        #Imprimimos toda la lista de instrucciones
        if self.list_inst:
            for inst in self.list_inst:
                inst.printTree(level + 1)
      
        printValueIdented("BLOCK_END", level)

    def symbolcheck(self):
        
        if self.declaraciones:
            empilar(self.declaraciones, self.alcance)
            self.declaraciones.symbolcheck()
        if self.list_inst:
            for inst in self.list_inst:
                empilar(inst, self.alcance)
                inst.symbolcheck()
        return True
 
#Clase para las declaraciones
class Using(Expression):
 
    def __init__(self, list_declare):
        self.type         = "USING"
        self.list_declare = list_declare
        self.alcance      = tablaSimbolos()
 
    def printTree(self,level):
        printValueIdented(self.type, level)
        #Se imprimen todas las declaraciones
        for declaration in self.list_declare:
            declaration.printTree(level)
        printValueIdented("IN", level)

    def symbolcheck(self):
        for declaration in self.list_declare:
            empilar(declaration, self.alcance)
            declaration.symbolcheck()

class Declaration(Expression):
 
    def __init__(self, decType, list_id):
        self.type    = decType
        self.list_id = list_id
        self.alcance = tablaSimbolos()
 
    def printTree(self, level):
        self.type.printTree(level)
        for identifier in self.list_id:
            printValueIdented(identifier, level + 2)

    def symbolcheck(self):
        for var in self.list_id:
            self.alcance.insert(var, self.type.type)

#Clase para los condicionales
class If(Expression):   
    
    def __init__(self,condition,inst_if,inst_else = None):
        self.type      = 'IF'
        self.condition = condition
        self.inst_if   = inst_if
        self.inst_else = inst_else 

    def printTree(self,level):
        printValueIdented(self.type,level)
        printValueIdented("condition",level + 1)
        self.condition.printTree(level + 2)
        printValueIdented('THEN',level + 1)
        self.inst_if.printTree(level + 2)

        if self.inst_else is not None:
            printValueIdented('ELSE',level)
            self.inst_else.printTree(level +1)
        printValueIdented('END_IF',level)

    def symbolcheck(self):
        empilar(self.condition, self.alcance)
        
        conditionType = self.condition.symbolcheck()

        if self.inst_else:
            empilar(self.inst_else, self.alcance)
            inst_else_Type = self.inst_else.symbolcheck()

        if conditionType != 'bool':
            mensaje = "ERROR: La condicion del if no es booleana"
            type_error_list.append(mensaje) 

class For(Expression):
    
    def __init__(self,identifier,direction,expre,inst):
        self.type       = 'FOR'
        self.identifier = identifier
        self.direction  = direction
        self.expre      = expre
        self.inst       = inst

    def printTree(self,level):
        printValueIdented(self.type,level)
        self.identifier.printTree(level + 1)
        self.direction.printTree(level + 1)
        printValueIdented('IN',level + 1)
        self.expre.printTree(level + 1)
        printValueIdented('DO',level + 1)
        self.inst.printTree(level + 2)
        printValueIdented('END_FOR',level)

    def symbolcheck(self):
        #Creamos la tabla para el alcance local del for        
        alcanceFor = tablaSimbolos()
        alcanceFor.parent = self.alcance
        alcanceFor.insert(self.identifier, 'int', False)
        self.alcance.children.append(alcanceFor)
        
        empilar(self.expre, self.alcance)
        empilar(self.inst, alcanceFor)

        expreType = self.expre.symbolcheck()

        if expreType != 'set':
            mensaje = "ERROR: La expresion " + self.expre\
                      + " debe ser de tipo 'set'."   
            type_error_list.append(mensaje) 

class Direction(Expression):
    
    def __init__(self,value):
        self.type  = 'direction'
        self.value = value

    def printTree(self,level):
        printValueIdented(self.type, level)
        printValueIdented(self.value,level + 1)

class RepeatWhileDo(Expression):
    
    def __init__(self,inst1,expre,inst2):
        self.type  = 'REPEAT'
        self.inst1 = inst1
        self.expre = expre
        self.inst2 = inst2

    def printTree(self,level):
        printValueIdented(self.type,level)
        self.inst1.printTree(level + 1)
        printValueIdented('WHILE',level)
        printValueIdented('condition', level + 1)
        self.expre.printTree(level + 2)
        printValueIdented('DO',level)
        self.inst2.printTree(level + 1)

    def symbolcheck(self):
        
        empilar(self.inst1, self.alcance)
        empilar(self.expre, self.alcance)
        empilar(self.inst2, self.alcance)

        expreType = self.expre.symbolcheck()
        #Verificamos que la condicion sea booleana
        if expreType != 'bool':
            mensaje = "La condicion del while debe ser de tipo 'bool'."
            type_error_list.append(mensaje)        

#Clase para los ciclos while condicion do
class WhileDo(Expression):
    
    def __init__(self,expre,inst):
        self.type  = 'WHILE'
        self.expre = expre
        self.inst  = inst
    
    def printTree(self, level):
        printValueIdented(self.type,level)
        printValueIdented('condition',level + 1)
        self.expre.printTree(level + 2)
        printValueIdented('DO',level)
        self.inst.printTree(level + 1)
        printValueIdented('END_WHILE',level)

    def symbolcheck(self):
        
        empilar(self.expre, self.alcance)
        empilar(self.inst, self.alcance)

        expreType = self.expre.symbolcheck()
        #Verificamos que la condicion sea booleana
        if expreType != 'bool':
            mensaje = "La condicion del while debe ser de tipo 'bool'."
            type_error_list.append(mensaje) 
            
#Clase para los ciclos repeat instruccion while condicion do
class RepeatWhile(Expression):
    
    def __init__(self,inst,expre):
        self.type  = 'REPEAT'
        self.inst  = inst
        self.expre = expre
        
    def printTree(self,level):
        printValueIdented(self.type,level)
        self.inst.printTree(level + 1)
        printValueIdented('condition',level + 1)
        self.expre.printTree(level + 2) 

    def symbolcheck(self):

        empilar(self.inst, self.alcance)
        empilar(self.expre, self.alcance)

        expreType = self.expre.symbolcheck()
        #Verificamos que la condicion sea booleana
        if expreType != 'bool':
            mensaje = "La condicion del while debe ser de tipo 'bool'."
            type_error_list.append(mensaje) 

class Number(Expression):
    
    def __init__(self, number):
        self.type   = "int"
        self.number = number

    def printTree(self, level):
        printValueIdented(self.type, level)
        printValueIdented(self.number, level + 1)

    def symbolcheck(self):
        return 'int'

# Clase para definir un string o cadena de caracteres.
class String(Expression):

    def __init__(self, string):
        self.type   = "STRING"
        self.string = string

    def printTree(self, level):
        printValueIdented(self.type, level)
        printValueIdented(self.string, level + 1)

    def symbolcheck(self):
        return 'string'

# Clase para definir un identificador o variable.
class Identifier(Expression):

    def __init__(self, identifier):
        self.type       = "VARIABLE"
        self.identifier = identifier
        self.alcance    = tablaSimbolos()

    def __str__(self):
        return self.identifier

    def printTree(self, level):
        printValueIdented(self.type, level)
        printValueIdented(self.identifier, level + 1)

    def symbolcheck(self): 

        if self.alcance.globalContains(self.identifier):
            identifier = self.alcance.buscar(self.identifier)
            return identifier.type
        else:
            mensaje =   "ERROR: Variable '" + str(self.identifier)\
                      + "' es asignada antes de ser declarada." 
            type_error_list.append(mensaje)

            return str(self.identifier)

# Clase para definir una expresion booleana.
class Bool(Expression):
    
    def __init__(self, value):
        self.type  = 'bool'
        self.value = value

    def printTree(self,level):
        printValueIdented(self.type, level)
        printValueIdented(self.value, level + 1)

    def symbolcheck(self):
        return 'bool'

class Parenthesis(Expression):
    
    def __init__(self, exp):
        self.type = 'PARENTHESIS'
        self.exp  = exp
        self.alcance = tablaSimbolos()

    def printTree(self,level):
        printValueIdented(self.type, level)
        self.exp.printTree(level + 1)

    def symbolcheck(self):
        empilar(self.exp, self.alcance)
        return self.exp.symbolcheck()

# Clase para definir un Conjunto.
class Set(Expression):
 
    def __init__(self,list_expr):
        self.type = 'SET'
        self.list_expr = list_expr
 
    def printTree(self,level):
        printValueIdented(self.type, level)
        if self.list_expr:
            for expr in self.list_expr:
                expr.printTree(level + 1)

    def symbolcheck(self):
        if self.list_expr:
            # Un set solo puede contener numeros
            type_set = 'int'
            for exp in self.list_expr:
                if type_set != exp.symbolcheck():
                    mensaje = "SET esperaba un numero entero pero se encontro Variable '" \
                             + exp.symbolcheck() + "'."
                    type_error_list.append(mensaje)
                    return exp.symbolcheck()
            return 'set'

# Clase para definir los tipos.
class Type(Expression):

    def __init__(self, typeName):
        self.type = typeName
 
    def printTree(self,level):
        printValueIdented(self.type, level + 1)

#Classe para los Operadores Binarios
class BinaryOperator(Expression):

    global binaryOperatorTypeTuples
    binaryOperatorTypeTuples = {
            ('int', 'TIMES', 'int'): 'int',
            ('int', 'PLUS', 'int'): 'int',
            ('int', 'MINUS', 'int'): 'int',
            ('int', 'DIVIDE', 'int'): 'int',
            ('int', 'MODULE', 'int'): 'int',
            ('set', 'UNION', 'set'): 'set',
            ('set', 'DIFERENCE','set'): 'set',
            ('set', 'INSERSECTION','set'):'set',
            ('int', 'PLUSMAP', 'set'): 'set',
            ('int', 'MINUSMAP', 'set'): 'set',
            ('int', 'TIMESMAP', 'set'): 'set',
            ('int', 'DIVIDEMAP','set'): 'set',
            ('int', 'MODULEMAP', 'set'): 'set',
            ('bool', 'OR', 'bool'): 'bool',
            ('bool', 'AND', 'bool'): 'bool',
            ('int', 'LESS','int'): 'bool',
            ('int', 'GREAT', 'int'): 'bool',
            ('int', 'LESSEQ', 'int'): 'bool',
            ('int', 'GREATEQ', 'int'): 'bool',
            ('int', 'EQUAL', 'int'): 'bool',
            ('bool', 'EQUAL', 'bool'): 'bool',
            ('set', 'EQUAL', 'set'): 'set',
            ('int', 'UNEQUAL', 'int'): 'bool',
            ('bool', 'UNEQUAL', 'bool'): 'bool',
            ('set', 'UNEQUAL', 'set'): 'bool',
            ('int', 'CONTAINMENT', 'set'): 'bool'
        }
 
    def __init__(self, lefExp, operator, rightExp):
        self.lefExp   = lefExp
        self.operator = Operator(operator)
        self.rightExp = rightExp
        self.alcance  = tablaSimbolos()
 
    def printTree(self, level):
        self.operator.printTree(level)
        self.lefExp.printTree(level + 1)
        self.rightExp.printTree(level + 1)

    def symbolcheck(self):
        #Pasamos la tabla de simbolos
        empilar(self.lefExp, self.alcance)
        empilar(self.rightExp, self.alcance)
        #Verificamos los tipos de cada operando
        lefExpType     = self.lefExp.symbolcheck()
        rightExpType   = self.rightExp.symbolcheck()
        operatorName   = self.operator.symbolcheck()

        print lefExpType, operatorName ,rightExpType

        newTuple = (lefExpType, operatorName, rightExpType)
        if newTuple in binaryOperatorTypeTuples:
            return binaryOperatorTypeTuples[newTuple]
        else:
            mensaje = "ERROR: No se puede aplicar '" + self.operator.name\
                      + "' en operandos de tipo '" + lefExpType\
                      + "' y '" + rightExpType + "'."
            type_error_list.append(mensaje)
            return False

#Clase para los Oeradores Unarios
class UnaryOperator(Expression):
    
    def __init__(self,operator,expresion):
        self.operator  = Operator(operator)
        self.expresion = expresion

    def printTree(self,level):
        self.operator.printTree(level)
        self.expresion.printTree(level + 1)

# Classe para los operadores:
class Operator(Expression):
 
    #Todos ellos. Sin distincion Binaria/Unaria
    global operator_dicc
    operator_dicc = {
        '*'  :'TIMES',
        '+'  :'PLUS',
        '-'  :'MINUS',
        '/'  :'DIVIDE',
        '%'  :'MODULE',
        '++' :'UNION',
        '\\' :'DIFERENCE',
        '><' :'INTERSECTION',
        '<+>':'PLUSMAP',
        '<->':'MINUSMAP',
        '<*>':'TIMESMAP',
        '</>':'DIVIDEMAP',
        '<%>':'MODULEMAP',
        '>?' :'MAXVALUE',
        '<?' :'MINVALUE',
        '$?' :'NUMELEMENTS',
        'or' :'OR',
        'and':'AND',
        'not':'NOT',        
        '@'  :'CONTAINMENT',
        '<'  :'LESS',
        '>'  :'GREAT',
        '<=' :'LESSEQ',
        '>=' :'GREATEQ',
        '==' :'EQUAL',
        '/=' :'UNEQUAL',        
    }

################################################################################

    def __init__(self,operator):
        self.operator = operator
        self.name     = operator_dicc[operator]

    def __str__(self):
        return self.name
 
    def printTree(self,level):
        printValueIdented(self.name +" "+ self.operator, level)

    def symbolcheck(self):
        return self.name
