# code parser here

from error import *
from error import WinkySyntaxError
from model import *
from tokens import *


class Parser:
    def __init__(self , tokens):
        self.tokens = tokens
        self.curr = 0
    

    def advance(self):
        token = self.peek()
        self.curr += 1
        return token

    def peek(self) -> Token:
        return self.tokens[self.curr]

    def isNext(self , expected_type : Token):
        if self.next_token().token_type == expected_type:
            return True
        else: return False

    def expect(self , expected_type):
        if self.curr >= len(self.tokens):
            WinkySyntaxError(f"Found {self.prev_token().lexeme!r} at the end of parsing." , self.prev_token().line)
        if self.peek().token_type == expected_type:
            token = self.advance()
            return token
        else: WinkySyntaxError(f"Expected {expected_type!r} but found {self.peek().lexeme!r}." , self.prev_token().line)
    
    def match(self,expected): 
        if self.curr < len(self.tokens) and self.peek().token_type == expected:
            self.curr += 1
            return True
        else: return False
    

    def prev_token(self) -> Token:
        return self.tokens[self.curr -1]    


    def next_token(self) -> Token:
        if (self.curr +1) <= len(self.tokens):
            return self.tokens[self.curr +1]
        else : WinkySyntaxError(f"Found {self.prev_token().lexeme!r} at the end of parsing." , self.prev_token().line)

    # <primary  > ::=  <number> | <bool> | <string> | '('<expr>')'
    # <number>  ::=  <digit>+
    # <digit>   ::=  '0' | '1' | '2' | ... | '9'
    # <bool>    ::=  'true' | 'false'
    def primary(self):
        if self.match(TOK_INTEGER) : return Integer(int(self.prev_token().lexeme) , line=self.prev_token().line)
        if self.match(TOK_FLOAT) : return Integer(float(self.prev_token().lexeme) , line=self.prev_token().line)
        if self.match(TOK_TRUE) : return Bool(bool(self.prev_token().lexeme) , line=self.prev_token().line)
        if self.match(TOK_FALSE) : return Bool(bool(self.prev_token().lexeme) , line=self.prev_token().line)
        if self.match(TOK_STRING) : return String(str(self.prev_token().lexeme[1:-1]) , line=self.prev_token().line)
        if self.match(TOK_LPAREN):
            expr = self.expr()
            if not(self.match(TOK_RPAREN)) : WinkySyntaxError("unexpected errpr : needed a ')'" , self.prev_token().line)
            else : return Grouping(expr , line=self.prev_token().line)
    
    # <unary> ::= ('+' | '-' | '~') <unary> | <primary>
    def unary(self):
        if self.match(TOK_PLUS) or self.match(TOK_MINUS) or self.match(TOK_NOT):
            op = self.prev_token()
            right = self.unary()
            return UnOp(op , right , line=self.prev_token().line)
        return self.primary()
    
    # <factor> ::= <unary>
    # factor is about multiplication or division
    def factor(self):
        return self.unary()

    # <term>  ::=  <factor> (<mulop> <factor>)*
    # <mulop> ::=  '*' | '/'
    # term is about addition or subtraction
    def term(self):
        factor = self.factor()
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            op = self.prev_token()
            right = self.factor()
            factor = BinOp(op , factor , right , line=self.prev_token().line)
        return factor
    
    # <expr>  ::=  <term> (<addop> <term>)*
    # <addop> ::=  '+' | '-'
    def expr(self):
        term = self.term()
        while self.match(TOK_PLUS) or self.match(TOK_MINUS):
            op = self.prev_token()
            right = self.term()
            term = BinOp(op , term , right , line=self.prev_token().line)
        return term

    def parse(self):
        ast = self.expr()
        return ast
