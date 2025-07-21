# code parser here

from error import *
from error import WinkySyntaxError
from model import *
from tokens import *
import tokens


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
        if self.curr >= len(self.tokens):
            return False
        if self.peek().token_type != expected:
            return False
        self.curr += 1
        return True
    

    def prev_token(self) -> Token:
        return self.tokens[self.curr -1]

    def next_token(self):
        if (self.curr +1) < len(self.tokens):
            return self.tokens[self.curr +1]
        else : WinkySyntaxError(f"Found {self.prev_token().lexeme!r} at the end of parsing." , self.prev_token().line)

    # <primary> ::=  <number> | <bool> | <string> | <identifier> | '('<expr>')'
    # <number>  ::=  <digit>+
    # <digit>   ::=  '0' | '1' | '2' | ... | '9'
    # <bool>    ::=  'true' | 'false'
    def primary(self):
        if self.match(TOK_INTEGER) : return Integer(int(self.prev_token().lexeme) , line=self.prev_token().line)
        elif self.match(TOK_FLOAT) : return Float(float(self.prev_token().lexeme) , line=self.prev_token().line)
        elif self.match(TOK_TRUE) : return Bool(True , line=self.prev_token().line)
        elif self.match(TOK_FALSE) : return Bool(False , line=self.prev_token().line)
        elif self.match(TOK_STRING) : return String(str(self.prev_token().lexeme[1:-1]) , line=self.prev_token().line)
        elif self.match(TOK_LPAREN):
            expr = self.OR()
            if (not self.match(TOK_RPAREN)) : WinkySyntaxError("unexpected error : needed a ')'" , self.prev_token().line)
            else : return Grouping(expr , line=self.prev_token().line)
        else:
            identifier = self.expect(TOK_IDENTIFIER)
            if self.match(TOK_LPAREN):
                args = self.args()
                self.expect(TOK_RPAREN)
                return FuncCall(identifier.lexeme,args , line=self.prev_token().line)
            else:
                return Identifier(identifier.lexeme , line=self.prev_token().line)

    # <Expo> ::= <primary> ('^' <primary>)*
    def Expo(self):
        primary = self.primary()
        while self.match(TOK_CARET):
            op = self.prev_token()
            # we want that the exponent operator be right associative so we call the rhs recursivly
            right = self.Expo()
            primary = BinOp(op , primary , right , line=self.prev_token().line)
        return primary


    # <unary> ::= ('+' | '-' | '~') <unary> | <Parenthes>
    def unary(self):
        if self.match(TOK_PLUS) or self.match(TOK_MINUS) or self.match(TOK_NOT):
            op = self.prev_token()
            right = self.unary()
            return UnOp(op , right , line=self.prev_token().line)
        return self.Expo()

    # <Mod> ::= <Unary> ('%' <Unary>)*
    def Mod(self):
        unary = self.unary()
        while self.match(TOK_MOD):
            op = self.prev_token()
            right = self.unary()
            unary = BinOp(op , unary , right , line=self.prev_token().line)
        return unary

    # <term>  ::=  <Mod> (<mulop> <Mod>)*
    # <mulop> ::=  '*' | '/' 
    # term is about addition or subtraction
    def term(self):
        factor = self.Mod()
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            op = self.prev_token()
            right = self.Mod()
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
    

    # <COMPA> ::= <expr> (('<' | '>' | '<=' | '>=') <expr>)*
    def COMPA(self):
        expr = self.expr()
        while self.match(TOK_GT) or self.match(TOK_LT) or self.match(TOK_GE) or self.match(TOK_LE):
            op = self.prev_token()
            right = self.expr()
            expr = BinOp(op , expr , right , line=self.prev_token().line)
        return expr

    # <EQUAL> ::= <COMPA> (('==' | '~=') <COMPA>)*
    def EQUAL(self):
        compa = self.COMPA()
        while self.match(TOK_EQEQ) or self.match(TOK_NE):
            op = self.prev_token()
            righ = self.COMPA()
            compa = BinOp(op , compa , righ , line=self.prev_token().line)
        return compa

    # <AND> ::= <EQUAL> ('and' <EQUAL>)*
    def AND(self):
        equal = self.EQUAL()
        while self.match(TOK_AND):
            op = self.prev_token()
            right = self.EQUAL()
            equal = LogicalOp(op , equal , right , line=self.prev_token().line)
        return equal

    # <OR> ::= <AND> ('or' <AND>)*  
    def OR(self):
        And = self.AND()
        while self.match(TOK_OR):
            op = self.prev_token()
            right = self.AND()
            And = LogicalOp(op , And , right , line=self.prev_token().line)
        return And
    
    def print_stmt(self , end):
        if self.match(TOK_PRINT) or self.match(TOK_PRINTLN):
            val = self.OR()
            return PrintStmt(val , line=self.prev_token().line ,end=end)
      
      
    # <ifStmt> ::= "if" <test_expr> "then" <then_stmt> ("else" <else_stmt>)? "end"
    def if_stmt(self):
        self.expect(TOK_IF)
        test_expr = self.OR()
        self.expect(TOK_THEN)
        then_stmt = self.stmts()
        if self.peek().token_type == TOK_ELSE:
            self.advance()
            else_stmt = self.stmts()
        else:
            else_stmt = None

        self.expect(TOK_END)
        return IfStmt(test_expr , then_stmt , else_stmt , line=self.prev_token().line)

    # <whileStmt> ::= "while" <text_expr> "do" <while_stmts> "end"
    def while_stmt(self):
        self.expect(TOK_WHILE)
        test_expr = self.OR()
        self.expect(TOK_DO)
        while_stmts = self.stmts()
        self.expect(TOK_END)
        return WhileStmt(test_expr , while_stmts , line=self.prev_token().line)


    # <forStmt> ::= "for" <assignment> , <expr> , (<expr>)? "do" <for_stmts> end
    def for_stmt(self):
        self.expect(TOK_FOR)
        identifier = self.primary()
        self.expect(TOK_ASSIGN)
        start_exp = self.OR()
        self.expect(TOK_COMMA)
        end_expr = self.OR()
        stepper_expr = None
        if self.peek().token_type == TOK_COMMA:
            self.expect(TOK_COMMA)
            stepper_expr = self.OR()
        self.expect(TOK_DO)
        for_stmts = self.stmts()
        return ForStmt(identifier, start_exp , end_expr , stepper_expr , for_stmts , line=self.prev_token().line)
   
    
    def args(self):
        args = []
        while not self.peek().token_type == TOK_RPAREN:
            arg = self.OR()
            args.append(arg)
            if not self.peek().token_type == TOK_RPAREN:
                self.expect(TOK_COMMA)
        return args

    def params(self):
        params = []
        while not self.peek().token_type == TOK_RPAREN:
            name = self.expect(TOK_IDENTIFIER)
            params.append(Param(name.lexeme , line=self.prev_token().line))
            if not self.peek().token_type == TOK_RPAREN:
                self.expect(TOK_COMMA)
        return params
    
    #<func_decl> ::= "func" <name> "(" <params>? ")" <body_stmts> "end"
    def func_decl(self):
        self.expect(TOK_FUNC)
        name = self.expect(TOK_IDENTIFIER)
        self.expect(TOK_LPAREN)
        params = self.params()
        self.expect(TOK_RPAREN)
        body_stmts = self.stmts()
        self.expect(TOK_END)
        return FuncDecl(name.lexeme , params , body_stmts , line=self.prev_token().line)

    
    def ret_stmt(self):
        self.expect(TOK_RET)
        expr = self.OR()
        return RetStmt(expr , line=self.prev_token().line)

    
    # <stmt>    ::=     print_stmt
    #               |   if_stmt
    #               |   while_stmt
    #               |   for_stmt
    #               |   func_decl
    #               |   func_call
    #               |   ret_stmt                                  
    def stmt(self):
        #TODO: parse for assignment , while , if , else , print , end , etc , here.
        if self.peek().token_type == TOK_PRINT:
            return self.print_stmt(end="")
        elif self.peek().token_type == TOK_PRINTLN:
            return self.print_stmt(end = "\n")
        elif self.peek().token_type == TOK_IF:
            return self.if_stmt()
        elif self.peek().token_type == TOK_WHILE:
            return self.while_stmt()
        elif self.peek().token_type == TOK_FOR:
            return self.for_stmt()
        elif self.peek().token_type == TOK_FUNC:
            return self.func_decl()
        elif self.peek().token_type == TOK_RET:
            return self.ret_stmt()
        else:
            #handle identifier and function call here.
            left = self.OR()
            if self.match(TOK_ASSIGN):
                right = self.OR()
                return Assignment(left , right , line=self.prev_token().line)
            else:
                # handle functoin call statement here.
                return FuncCallStmt(left)

    def stmts(self):
        stmts = []
        while self.curr < len(self.tokens) and not self.peek().token_type == TOK_ELSE and not self.peek().token_type == TOK_END:
            stmt = self.stmt()
            stmts.append(stmt)
        return Stmts(stmts , line=self.prev_token().line)

    def program(self):
        stmts = self.stmts()
        return stmts

    def parse(self):
        program = self.program()
        return program
