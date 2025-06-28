# code object here.

from tokens import Token

class Expr:
    '''
    Expresion evaluate to a result
    '''
    pass


class Stmt:
    '''
    Statement perform an action
    '''
    pass


class Integer(Expr):
    def __init__(self ,value):
        assert isinstance(value , int) , value
        self.value = value

    def __repr__(self) -> str:
        return f"Integer [{self.value}]"


class Float(Expr):
    def __init__(self , value):
        assert isinstance(value , float) , value
        self.value = value

    def __repr__(self) -> str:
        return f"Float [{self.value}]"

class UnOp(Expr):
    '''
    Example : -20
    '''
    def __init__(self , op : Token , value : Expr):
        assert isinstance(op , Token) , op
        assert isinstance(value , Expr) , value
        self.op = op
        self.value = value

    def __repr__(self) -> str:
        return f"Unary Operator [{self.op.lexeme}{self.value}]"



class BinOp(Expr):
    '''
    Example : 10 + 12 * 3 / 4
    '''
    def __init__(self , op : Token , left : Expr , right : Expr):
        assert isinstance(op , Token) , op
        assert isinstance(left , Expr) , left
        assert isinstance(right , Expr) , right
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Binary Operator :  Operator: [{self.op.lexeme} , LHS: [{self.left}] , RHS: [{self.right}]]"


class Grouping(Expr):
    '''
    Example : ( <expr> )
    '''
    def __init__(self , value : Expr):
        assert isinstance(value , Expr) , value
        self.value = value

    def __repr__(self) -> str:
        return f"Grouping( {self.value} )"


class WhileStmt(Stmt):
    pass

class Assignment(Stmt):
    pass
