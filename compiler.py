# code compier here.
# compiler generate the byte-code assocaited to souce code

from model import *
from tokens import *
from utils import *

TYPE_NUMBER = "TYPE_NUMBER"
TYPE_STRING = "TYPE_STRING"
TYPE_BOOL   = "TYPE_BOOL"

class Compiler:
    def __init__(self) -> None:
        self.code = []

    def emit(self , instruction : tuple):
        self.code.append(instruction)    
    
    def compile(self , node):
        if isinstance(node , Integer):
            value = (TYPE_NUMBER , float(node.value))
            self.emit(('PUSH' , value))
        
        if isinstance(node , Float):
            value = (TYPE_NUMBER , float(node.value))
            self.emit(('PUSH' , value))
        
        if isinstance(node , String):
            value = (TYPE_STRING , node.value)
            self.emit(('PUSH' , value))
        
        if isinstance(node , Bool):
            value = ()
            if node.value:
                value = (TYPE_BOOL , 1)
            else:
                value = (TYPE_BOOL , 0)
            self.emit(('PUSH' , value))


        
        if isinstance(node , BinOp):
            self.compile(node.left)
            self.compile(node.right)
            
            op = node.op.token_type
            if op == TOK_PLUS:
                self.emit(('ADD',))


        if isinstance(node , PrintStmt):
            self.compile(node.value)
            self.emit(('PRINT',))

        if isinstance(node , Stmts):
            for stmt in node.stmts:
                self.compile(stmt)

    

    def compile_code(self , node) -> list:
        self.compile(node)
        return self.code
