# code parser here

from model import *
from tokens import *


class Parser:
    def __init__(self , tokens):
        self.tokens = tokens
        self.curr = 0
        self.ast = []
    
    def match(self,expected): 
        if self.curr < len(self.tokens) and self.curr_token().token_type == expected:
            self.curr += 1
            return True
        else: return False
    

    def prev_token(self , n=1):
        return self.tokens[self.curr -n]    

    def curr_token(self):
        return self.tokens[self.curr]

    def next_token(self):
        if (self.curr +1) <= len(self.tokens):
            return self.tokens[self.curr +1]



    def primary(self):
        if self.match(TOK_INTEGER) : return Integer(int(self.prev_token().lexeme))
        if self.match(TOK_FLOAT) : return Integer(float(self.prev_token().lexeme))
        if self.match(TOK_LPAREN):
            expr = self.expr()
            if not(self.match(TOK_RPAREN)) : raise SyntaxError("unexpected errpr : needed a ')'")
            else : return Grouping(expr)

    def unary(self):
        if self.match(TOK_PLUS) or self.match(TOK_MINUS) or self.match(TOK_NOT):
            op = self.prev_token()
            right = self.unary()
            return UnOp(op , right)
        return self.primary()

    def factor(self):
        return self.unary()

    def term(self):
        factor = self.factor()
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            op = self.prev_token()
            right = self.factor()
            factor = BinOp(op , factor , right)
        return factor

    def expr(self):
        term = self.term()
        while self.match(TOK_PLUS) or self.match(TOK_MINUS):
            op = self.prev_token()
            right = self.term()
            term = BinOp(op , term , right)
        return term

    def parse(self):
        ast = self.expr()
        return ast
