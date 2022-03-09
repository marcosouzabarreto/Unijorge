# IMPORTS

# Lexer generator
import ply.lex as lex
# Parser generator
import ply.yacc as yacc

# Tokenize expression
# 1 + 2 should come out like INT(1), PLUS, INT(2)

tokens = [
    'PLUS',
    'MINUS',
    'DIVISION',
    'MULTIPLICATION',
    'INT',
    'FLOAT',
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVISION = r'\*'
t_MULTIPLICATION = r'\/'

t_ignore = r' '  # Ignore spaces in the expression


def t_FLOAT(t):
    r"""\d+\.\d+"""  # Pegar número inteiro que depois dele venha um ponto, e depois outro numero
    t.value = float(t.value)
    return t


def t_INT(t):
    r"""\d+"""  # Pegar numero inteiro com tamanho maior ou igual à 1
    t.value = int(t.value)
    return t


def t_error(t):
    print('erro, caractere inválido')
    t.lexer.skip(1)


lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLICATION', 'DIVISION')
)


def p_calc(p):
    # Criar regras de gramática

    # Calculo pode ser ou uma expressão ou nada
    # Preciso desse empty pois se o usuário não digitar nada, eu recebo vários parse errors
    """
    calc : expression
         | empty
    """
    print(execute_calculator(p[1]))


def p_expression(p):
    # Essa parte serve para poder usar infinitas somas, e não só 1
    # ex: antes não poderia usar 1+1+1, só aceitava 1+1
    """
    expression : expression MULTIPLICATION expression
               | expression DIVISION expression
               | expression PLUS expression
               | expression MINUS expression

    """
    # p[0] = expression, p[1] recursive expression 1, p[2] = TOKEN, p[3] recursive expression 2
    # Criar uma ordem de execução para a calculadora tipo uma árvore
    # ex: 1 + 2 * 3 vira um tuple assim: ('+', 1, ('*', 2, 3))
    # facilitando a criada de ordem de execução

    p[0] = (p[2], p[1], p[3])


def p_int_of_float_expression(p):
    """
    expression : INT
               | FLOAT
    """
    p[0] = p[1]


def p_error(p):
    print('Erro de sintaxe')


def p_empty(p):
    """
    empty :
    """
    p[0] = None


parser = yacc.yacc(debug=False, write_tables=False)


def execute_calculator(expression):
    if type(expression) == tuple:

        # Recursivamente pegar todas as partes da expressão e mandar para essa função,
        # sendo que expression[1] é a parte esquerda da conta
        # e expression[2] é a parte da direita, se mandar para essa função de execute_calculator
        # e ela for um número, ele para a execução e a recursao está completa,
        # senão, ele volta novamente para a função, separando a expressao novamente

        if expression[0] == '+':
            return execute_calculator(expression[1]) + execute_calculator(expression[2])
        elif expression[0] == '-':
            return execute_calculator(expression[1]) - execute_calculator(expression[2])
        elif expression[0] == '*':
            return execute_calculator(expression[1]) * execute_calculator(expression[2])
        elif expression[0] == '/':
            return execute_calculator(expression[1]) / execute_calculator(expression[2])
    else:
        return expression


while True:
    try:
        user_input = input('Digite a operação: >> ')
    except EOFError:
        break
    parser.parse(user_input)
