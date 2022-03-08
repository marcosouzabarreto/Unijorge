# IMPORTS

# Lexer generator
import ply.lex as lex
# Parser generator
import ply.yacc as yacc
import sys

# Tokenize expression
# 1 + 2 should come out like INT(1), PLUS, INT(2)

tokens = [
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'INT',
    'FLOAT',
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'

t_ignore = r' '


def t_FLOAT(t):
    r"""\d+\.\d+"""
    t.value = float(t.value)
    return t


def t_INT(t):
    r"""\d+"""  # Get every number whose length is more than 1
    t.value = int(t.value)
    return t


def t_error(t):
    print('erro, caractere inválido')
    t.lexer.skip(1)


lexer = lex.lex()

lexer.input("1+3.2")


def p_calculadora(p):
    # Create grammar rules
    """

    """


while True:
    try:
        s = input('')
    except EOFError:
        break
