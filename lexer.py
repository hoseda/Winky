# the lexer codes are here.

from tokens import *

class Lexer:
    def __init__(self,source):
        self.source = source
        self.start = 0
        self.curr = 0
        self.line = 1
        self.tokens = []
    
    def add_token(self,token_type):
        self.tokens.append(Token(token_type , self.source[self.start:self.curr]))

    def advance(self):
        ch = self.source[self.curr]
        self.curr += 1
        return ch

    def peek(self):
        return self.source[aself.curr]

    
    def lookAhead(self , n =1):
        return self.source[self.curr + n]

    def match(self , expected):
        if self.source[self.curr] != expected:
            return False

        self.curr +=1
        return True


    def tokenize(self):
        while self.curr < len(self.source):
            self.start = self.curr
            ch = self.advance()
            
            #######################################################################
            ################## Tokenize the Single Characters #####################
            #######################################################################
            
            if ch == '+' : self.add_token(TOK_PLUS)
            if ch == '-' : self.add_token(TOK_MINUS)
            if ch == '*' : self.add_token(TOK_STAR)
            if ch == '.' : self.add_token(TOK_DOT)
            if ch == '/' : self.add_token(TOK_SLASH)
            if ch == '^' : self.add_token(TOK_CARET)
            if ch == ',' : self.add_token(TOK_COMMA)
            if ch == '%' : self.add_token(TOK_MOD)
            if ch == ':' : self.add_token(TOK_COLON)
            if ch == ';' : self.add_token(TOK_SEMICOLON)
            if ch == '?' : self.add_token(TOK_QUESTION)
            if ch == '>' : self.add_token(TOK_GT)
            if ch == '<' : self.add_token(TOK_LT)
            if ch == '~' : self.add_token(TOK_NOT)
            if ch == '(' : self.add_token(TOK_LPAREN) 
            if ch == ')' : self.add_token(TOK_RPAREN)
            if ch == '{' : self.add_token(TOK_LCURLY) 
            if ch == '}' : self.add_token(TOK_RCURLY)
            if ch == '[' : self.add_token(TOK_LSQUAR)
            if ch == ']' : self.add_token(TOK_RSQUAR)


        return self.tokens
