# code object here.

from sys import is_finalizing
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


class LogicalOp(Expr):
    def __init__(self , op : Token , left : Expr , right : Expr , line):
        assert isinstance(op , Token) , op
        assert isinstance(left , Expr) , left
        assert isinstance(right , Expr) , right
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self) -> str:
        return f"Logical Operator (Operator: [{self.op.lexeme}] , LHS: [{self.left}] , RHS: [{self.right}])"

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


class Identifier(Expr):
    '''
    Example: x , PI , _score , some_value , _forNow
    '''
    def __init__(self , lexeme , line):
        assert isinstance(lexeme , str) , lexeme
        self.lexeme = lexeme
        self.line = line

    def __repr__(self) -> str:
        return f"Identifier({self.lexeme})"

class Stmts(Node):
    '''
    contain the list of statements
    '''
    def __init__(self , stmts , line):
        assert all(isinstance(stmt , Stmt) for stmt in stmts)
        self.stmts = stmts
        self.line = line

    def __repr__(self) -> str:
        return f"Statements({self.stmts})"


class Assignment(Stmt):
    '''
    Example: x := 12 , y := x + 1
    '''
    def __init__(self , left , right , line):
        assert isinstance(left , Identifier), left
        assert isinstance(right , Expr), right
        self.left =left
        self.right =right
        self.line = line

    def __repr__(self) -> str:
        return f"Assigmnet({self.left} , {self.right})"

class PrintStmt(Stmt):
    '''
    print statement model
    '''
    def __init__(self , val , line , end):
        assert isinstance(val , Expr) , val
        self.value = val
        self.line = line
        self.end = end

    def __repr__(self) -> str:
        return f"PrintStmt({self.value} , end:{self.end!r})"


class PrintLnStmt(Stmt):
    '''
    print line statement model
    '''
    def __init__(self , val , line):
        assert isinstance(val , Expr) , val
        self.value = val
        self.line = line

    def __repr__(self) -> str:
        return f"PrintLnStmt({self.value})"

class WhileStmt(Stmt):
    '''
    while <test_expr> do
        <stmts>
    end
    '''
    def __init__(self , test_expr , while_stmts , line):
        assert isinstance(test_expr , Expr), test_expr
        assert isinstance(while_stmts , Stmts), while_stmts
        self.test_expr = test_expr
        self.while_stmts = while_stmts
        self.line = line

    def __repr__(self) -> str:
        return f"WhileStmt(test: [{self.test_expr}] , Stmts: [{self.while_stmts}])"


class IfStmt(Stmt):
    '''
    <ifStmt> ::= "if" <test_expr> "then" <then_stmt> ("else" <else_stmt>)? "end"
    '''
    def __init__(self , test_expr , then_stmt , else_stmt , line):
        assert isinstance(test_expr , Expr) , test_expr
        assert isinstance(then_stmt , Stmts) , then_stmt
        assert else_stmt is None or isinstance(else_stmt , Stmts) , else_stmt
        self.test_expr = test_expr
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt
        self.line = line

    def __repr__(self):
        return f"IfStmt(test:[{self.test_expr}] , then:[{self.then_stmt}] , else:[{self.else_stmt}])"

class ForStmt(Stmt):
    '''
    for <assignment> , <end> , (<stepper>)? do
        <stmts>
    end
    '''
    def __init__(self , identifier , start_expr , end_expr , stepper_expr , for_stmts , line):
        assert isinstance(identifier , Identifier) , identifier
        assert isinstance(start_expr , Expr) , start_expr
        assert isinstance(end_expr , Expr) , end_expr
        assert stepper_expr is None or isinstance(stepper_expr , Expr) , stepper_expr
        assert isinstance(for_stmts , Stmts) , for_stmts
        self.identifier = identifier
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.stepper_expr = stepper_expr 
        self.for_stmts = for_stmts
        self.line = line

    def __repr__(self) -> str:
        return f"ForStmt(StartAssignment: [{self.identifier}], StartExpr: [{self.start_expr}] , EndExpr: [{self.end_expr}] , StepperExpr: [{self.stepper_expr}] , Stmts: [{self.for_stmts}])"


