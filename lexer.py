# the lexer codes are here.

from error import WinkyLexerError
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
        if self.curr >= len(self.source):
            return '\0'
        return self.source[self.curr]

    def lookAhead(self , n =1):
        return self.source[self.curr + n]

    def match(self , expected):
        if self.source[self.curr] != expected:
            return False

        self.curr +=1
        return True


    def tokenize(self):
        print("inside tokenization loop")
        while self.curr < len(self.source):
            self.start = self.curr
            ch = self.advance()
            
            ########################################################
            #   Ignoring the Whitespace                            #
            ########################################################
            if   ch == '\n': self.line += 1
            elif ch == '\t': pass
            elif ch == '\r': pass
            elif ch == ' ' : pass

            ########################################################
            #   Single Character lexemes                           #
            ########################################################
            elif ch == '+' : self.add_token(TOK_PLUS)

            ########################################################
            # Ignoring Comments                                    #
            ########################################################

            elif ch == '-' :
                if self.peek() == '-':
                    while self.peek() != '\n' and not(self.curr > len(self.source)):
                        self.advance()
                else:
                    self.add_token(TOK_MINUS)
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
            elif ch == '}w' : self.add_token(TOK_RCURLY)
            #######################################################
            #   Two Character lexemes                             #
            #######################################################

            ## is equal ?
            elif ch == '=' :
                if self.match('=') : self.add_token(TOK_EQEQ)
                else : self.add_token(TOK_EQ)
            
            ## is not equal ?
            elif ch == '~' :
                if self.match('=') : self.add_token(TOK_NE)
                else : self.add_token(TOK_NOT)
            
            ## is grater than or equal ?
            elif ch == '>' :
                if self.match('=') : self.add_token(TOK_GE)
                elif self.match('>') : self.add_token(TOK_GTGT)
                else: self.add_token(TOK_GT)
            
            ## is less than or equal ?
            elif ch == '<' :
                if self.match('=') : self.add_token(TOK_LE)
                elif self.match('<') : self.add_token(TOK_LTLT)
                else: self.add_token(TOK_LT)
            
            ## assignment
            elif ch == ':' :
                if self.match('=') : self.add_token(TOK_ASSIGN)
                else : self.add_token(TOK_COLON)
            #########################################################
            #   Tokenize the Integer and Float                      #
            #########################################################
            elif ch.isdigit():
                 while self.peek().isdigit():
                     if self.curr < len(self.source):
                        self.advance()
                     else: return '\0'
                 if self.peek() ==  '.' and self.lookAhead().isdigit():
                     self.advance() # consume the dot.
                     while self.peek().isdigit():
                         if self.curr < len(self.source):
                             self.advance()
                         else: return '\0'
                     self.add_token(TOK_FLOAT)
                 else:
                     self.add_token(TOK_INTEGER)
            ########################################################
            #   Tokenize the String that start and end with ""     #
            ########################################################
            elif ch == '"':
                while self.peek() != '"':
                    if self.curr < len(self.source):
                        self.advance()
                    else: return '\0'
                if self.peek() == '"':
                    self.advance()
                    self.add_token(TOK_STRING)
                else: WinkyLexerError(f"Unexpected Character" , self.line)
            ########################################################
            #   Tokenize the String that start and end with ''     #
            ########################################################
            elif ch == "'":
                while self.peek() != "'":
                    if self.curr < len(self.source):
                        self.advance()
                    else: return '\0'
                if self.peek() == "'":
                    self.advance()
                    self.add_token(TOK_STRING)
                else: WinkyLexerError(f"UNexpected Character" , self.line)
            ########################################################
            #   Tokenize the Identifiers , Keywords                #
            ########################################################
            elif ch == "_" or ch.isalpha():
                while self.peek().isalnum() or self.peek() == '_':
                    if self.curr < len(self.source):
                        self.advance()
                    else: return '\0'
                text = self.source[self.start:self.curr]
                key_type = keywords.get(text)
                if key_type == None:
                    self.add_token(TOK_IDENTIFIER)
                else :self.add_token(key_type)

            else:
                WinkyLexerError(f"Unexpected Character {ch!r}" , self.line , self.curr)

        return self.tokens            
