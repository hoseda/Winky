# code compier here.
# compiler generate the byte-code assocaited to souce code

from model import *
from tokens import *
from utils import *


class Compiler:
    def __init__(self) -> None:
        self.code = []

    def emit(self , instruction : tuple):
        self.code.append(instruction)    
    
    def compile(self , node):
        if isinstance(node , Integer):
            value = (TYPE_NUMBER , float(node.value))
            self.emit(('PUSH' , value))
        
        elif isinstance(node , Float):
            value = (TYPE_NUMBER , float(node.value))
            self.emit(('PUSH' , value))
        
        elif isinstance(node , String):
            value = (TYPE_STRING , stringify(node.value))
            self.emit(('PUSH' , value))
        
        elif isinstance(node , Bool):
            value = ()
            if node.value:
                value = (TYPE_BOOL , True)
            else:
                value = (TYPE_BOOL , False)
            self.emit(('PUSH' , value))

        elif isinstance(node , BinOp):
            self.compile(node.left)
            self.compile(node.right)
            
            op = node.op.token_type
            if op == TOK_PLUS:
                self.emit(('ADD',))
            elif op == TOK_MINUS:
                self.emit(("SUB",))
            elif op == TOK_STAR:
                self.emit(("MUL",))
            elif op == TOK_SLASH:
                self.emit(("DIV",))
            elif op == TOK_CARET:
                self.emit(("EXP",))
            elif op == TOK_MOD:
                self.emit(("MOD",))
            elif op == TOK_EQEQ:
                self.emit(("EQ",))
            elif op == TOK_NE:
                self.emit(("NE",))
            elif op == TOK_GT:
                self.emit(("GT",))
            elif op == TOK_GE:
                self.emit(("GE",))
            elif op == TOK_LT:
                self.emit(("LT",))
            elif op == TOK_LE:
                self.emit(("LE",))
        
        elif isinstance(node , LogicalOp):
            self.compile(node.left)
            self.compile(node.right)

            op = node.op.token_type

            if op == TOK_OR:
                self.emit(("OR",))
            elif op == TOK_AND:
                self.emit(("AND",))

        elif isinstance(node , UnOp):
            self.compile(node.value)
            op = node.op.token_type

            if op == TOK_MINUS:
                self.emit(("NEG",))
            elif op == TOK_NOT:
                self.emit(("PUSH" , (TYPE_NUMBER, 1)))
                self.emit(("XOR",))

        elif isinstance(node , Grouping):
            self.compile(node.value)

        # compile statements here.

        elif isinstance(node , Stmts):
            for stmt in node.stmts:
                self.compile(stmt)

        elif isinstance(node , PrintStmt):
            self.compile(node.value)
            if node.end == "":
                self.emit(('PRINT',))
            else:
                self.emit(("PRINTLN",))

        elif isinstance(node , IfStmt):
            pass

        elif isinstance(node , ForStmt):
            pass

        elif isinstance(node , WhileStmt):
            pass

        elif isinstance(node , FuncDecl):
            pass

        elif isinstance(node , FuncCall):
            pass

        elif isinstance(node , FuncCallStmt):
            pass

        elif isinstance(node , RetStmt):
            pass 

    

    def generate_code(self , node) -> list:
        '''
        the starter function.
        returns a [List]
        '''
        self.emit(("LABLE" , "START"))
        self.compile(node)
        self.emit(("HALT",))
        return self.code
