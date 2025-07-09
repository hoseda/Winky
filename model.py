# code object here.

from typing import ValuesView
from tokens import Token


class Node:
    '''
    The parent class for every Node in AST.
    '''
    pass


class Expr(Node):
    '''
    Expresion evaluate to a result
    '''
    pass


class Stmt(Node):
    '''
    Statement perform an action
    '''
    pass


class Integer(Expr):
    def __init__(self ,value , line):
        assert isinstance(value , int) , value
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"Integer [{self.value}]"


class Float(Expr):
    def __init__(self , value , line):
        assert isinstance(value , float) , value
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"Float [{self.value}]"


class Bool(Expr):
    '''
    Example : true , false
    '''
    def __init__(self , value , line):
        assert isinstance(value , bool) , value
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"Bool[{self.value}]"


class String(Expr):
    '''
    Example : 'string' , "string"
    '''
    def __init__(self , value , line) -> None:
        assert isinstance(value , str) , value
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"String[{self.value}]"


class UnOp(Expr):
    '''
    Example : -20
    '''
    def __init__(self , op : Token , value : Expr , line):
        assert isinstance(op , Token) , op
        assert isinstance(value , Expr) , value
        self.op = op
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"Unary Operator ({self.op.lexeme},{self.value})"



class BinOp(Expr):
    '''
    Example : 10 + 12 * 3 / 4
    '''
    def __init__(self , op : Token , left : Expr , right : Expr , line):
        assert isinstance(op , Token) , op
        assert isinstance(left , Expr) , left
        assert isinstance(right , Expr) , right
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self) -> str:
        return f"Binary Operator (Operator: [{self.op.lexeme}] , LHS: [{self.left}] , RHS: [{self.right}])"


class Grouping(Expr):
    '''
    Example : ( <expr> )
    '''
    def __init__(self , value : Expr , line):
        assert isinstance(value , Expr) , value
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"Grouping({self.value})"


class WhileStmt(Stmt):
    pass

class Assignment(Stmt):
    pass

class IfStmt(Stmt):
    pass

class ForStmt(Stmt):
    pass
