import re

# Token types
class Token:
    NUMBER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = 'NUMBER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'EOF'

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

# Lexer class to tokenize the input
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        """Advance the position and update the current character."""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        """Skip over any whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a number token from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(Token.NUMBER, self.number())

            if self.current_char == '+':
                self.advance()
                return Token(Token.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(Token.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(Token.MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(Token.DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(Token.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(Token.RPAREN, ')')

            raise Exception(f"Invalid character: {self.current_char}")

        return Token(Token.EOF, None)

# Abstract Syntax Tree (AST) node base class
class AST:
    pass

# AST node for binary operations
class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

# AST node for numbers
class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Num({self.value})"

# Parser class
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, error_message):
        """Raise an error with the given message."""
        raise Exception(error_message)

    def eat(self, token_type):
        """Consume the current token if it matches the expected type."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected token {token_type}, got {self.current_token.type}")

    def factor(self):
        """Parse a factor (numbers and parenthesized expressions)."""
        token = self.current_token
        if token.type == Token.NUMBER:
            self.eat(Token.NUMBER)
            return Num(token)
        elif token.type == Token.LPAREN:
            self.eat(Token.LPAREN)
            node = self.expression()
            self.eat(Token.RPAREN)
            return node
        self.error("Invalid factor")

    def term(self):
        """Parse a term (factors separated by * or /)."""
        node = self.factor()
        while self.current_token.type in (Token.MUL, Token.DIV):
            token = self.current_token
            if token.type == Token.MUL:
                self.eat(Token.MUL)
            elif token.type == Token.DIV:
                self.eat(Token.DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expression(self):
        """Parse an expression (terms separated by + or -)."""
        node = self.term()
        while self.current_token.type in (Token.PLUS, Token.MINUS):
            token = self.current_token
            if token.type == Token.PLUS:
                self.eat(Token.PLUS)
            elif token.type == Token.MINUS:
                self.eat(Token.MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        """Parse the input and return the AST."""
        return self.expression()

# Main function to prompt user for input and parse it
def main():
    while True:
        try:
            text = input('calc> ')
            if not text:
                continue
            lexer = Lexer(text)
            parser = Parser(lexer)
            ast = parser.parse()
            print(ast)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
