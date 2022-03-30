# Imports
from constants import *

# Definição de erros


class Error:
    def __init__(self, error, details):
        self.error = error
        self.details = details

    def create_error_message(self):
        return f'Error: {self.error},\n {self.details}'


class CharacterNotDefined(Error):
    def __init__(self, details):
        super().__init__('Character not defined', details)


class InvalidSyntax(Error):
    def __init__(self, details):
        super().__init__('Invalid syntax', details)


# Tokenizador


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return self.type

# Analise léxica


class Lexer:
    def __init__(self, user_input):
        self.user_input = user_input
        self.current_pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.current_pos += 1
        self.current_char = self.user_input[self.current_pos] if self.current_pos < len(self.user_input) else None

    def create_numbers(self):
        num_as_string = ''
        dot_counter = 0
        while self.current_char is not None and self.current_char in NUMBERS + '.':
            if self.current_char == '.':
                if dot_counter >= 1:  # Um numero não pode ter mais de 1 ponto
                    break
                num_as_string += '.'
                dot_counter += 1
            else:
                num_as_string += self.current_char
            self.advance()
        if dot_counter == 0:
            return Token(T_INTEGER, int(num_as_string))
        else:
            return Token(T_FLOAT, float(num_as_string))

    def create_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in NUMBERS:
                tokens.append(self.create_numbers())
            elif self.current_char == '+':
                tokens.append(Token(T_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(T_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(T_MULTIPLY))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(T_DIVIDE))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(T_OPENROUNDBRACKETS))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(T_CLOSEROUNDBRACKETS))
                self.advance()
            else:
                invalid_char = self.current_char
                self.advance()
                return [], CharacterNotDefined(f"'{invalid_char}'")

        tokens.append(Token(T_EOF))
        return tokens, None

# Criar nós para fazer o parse


class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'


class BinaryOperationsNode:
    def __init__(self, left_node, operation_token, right_node):
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operation_token}, {self.right_node})'


class UnaryOperatorNode:
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node

    def __repr__(self):
        return f'({self.operator_token}, {self.node})'

# Parser


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        res = self.expression()
        if not res.error and self.current_token.type is not T_EOF:
            return res.failure(InvalidSyntax('Invalid Syntax'))
        return res

    def binary_operation(self, fun, operations):
        res = ParseResult()
        left = res.register(fun())
        if res.error:
            return res

        while self.current_token.type in operations:
            operation_token = self.current_token
            res.register(self.advance())
            right = res.register(fun())
            if res.error:
                return res
            left = BinaryOperationsNode(left, operation_token, right)
        return res.success(left)

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (T_MINUS, T_PLUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOperatorNode(token, factor))

        elif token.type == T_OPENROUNDBRACKETS:
            res.register(self.advance())
            expression = res.register(self.expression())
            if res.error:
                return res
            if self.current_token.type == T_CLOSEROUNDBRACKETS:
                res.register(self.advance())
                return res.success(expression)
            else:
                return res.failure(InvalidSyntax("Expected ')'"))

        elif token.type in (T_INTEGER, T_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(token))

        return res.failure(InvalidSyntax('Expected int or float'))

    def term(self):
        return self.binary_operation(self.factor, (T_MULTIPLY, T_DIVIDE))

    def expression(self):
        return self.binary_operation(self.term, (T_MINUS, T_PLUS))


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


# Rodar compilador
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.create_tokens()

    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
