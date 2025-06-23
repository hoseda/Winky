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
        self.tokens.append(Token(token_type , self.source[self.start:self.curr] , self.line))

    def advance(self):
        ch = self.source[self.curr]
        self.curr += 1
        return ch
    
    def peek(self):
        return self.source[self.curr]

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
            
            ########################################################
            #   Ignoring the Whitespace                            #
            ########################################################
            if   ch == '\n': self.line += 1
            elif ch == '\t': pass
            elif ch == '\r': pass
            ########################################################
            #   Ignoring the Comments                              #
            ########################################################
            elif ch == '#' :
                while self.peek() != '\n':
                    self.advance()
            ########################################################
            #   Single Character lexemes                           #
            ########################################################
            elif ch == '+' : self.add_token(TOK_PLUS)
            elif ch == '-' : self.add_token(TOK_MINUS)
            elif ch == '*' : self.add_token(TOK_STAR)
            elif ch == '.' : self.add_token(TOK_DOT)
            elif ch == '/' : self.add_token(TOK_SLASH)
            elif ch == '^' : self.add_token(TOK_CARET)
            elif ch == ',' : self.add_token(TOK_COMMA)
            elif ch == '%' : self.add_token(TOK_MOD)
            elif ch == ';' : self.add_token(TOK_SEMICOLON)
            elif ch == '?' : self.add_token(TOK_QUESTION)
            elif ch == '(' : self.add_token(TOK_LPAREN) 
            elif ch == ')' : self.add_token(TOK_RPAREN)
            elif ch == '{' : self.add_token(TOK_LCURLY)
            #######################################################
            #   Two Character lexemes                             #
            #######################################################
            elif ch == '=' :
                if self.match('=') : self.add_token(TOK_EQ)  
                
            elif ch == '~' :
                if self.match('=') : self.add_token(TOK_NE)
                else : self.add_token(TOK_NOT)

            elif ch == '>' :
                if self.match('=') : self.add_token(TOK_GE)
                elif self.match('>') : self.add_token(TOK_GTGT)
                else: self.add_token(TOK_GT)

            elif ch == '<' :
                if self.match('=') : self.add_token(TOK_LE)
                elif self.match('<') : self.add_token(TOK_LTLT)
                else: self.add_token(TOK_LT)
            
            elif ch == ':' :
                if self.match('=') : self.add_token(TOK_ASSIGN)
                else : self.add_token(TOK_COLON)




        return self.tokens
            
