# code Winky interpreter here.


from model import *
from tokens import *

class Interpreter:

    def interpret(self , node):
        if isinstance(node , Integer):
            return float(node.value)

        elif isinstance(node , Float):
            return float(node.value)

        elif isinstance(node , Grouping):
            return self.interpret(node.value)

        elif isinstance(node , BinOp):
            op_token = node.op.token_type
            lhs = self.interpret(node.left)
            rhs = self.interpret(node.right)

            if op_token == TOK_PLUS:
                return lhs + rhs
            
            elif op_token == TOK_MINUS:
                return lhs - rhs

            elif op_token == TOK_STAR:
                return lhs * rhs

            elif op_token == TOK_SLASH:
                return lhs / rhs

        
        elif isinstance(node , UnOp):
            operand_token = node.op.token_type
            expr = self.interpret(node.value)

            if operand_token == TOK_PLUS:
                return +expr

            elif operand_token == TOK_MINUS:
                return -expr

            #TODO: ADD NOT OPERAND ~ IN FUTURE

