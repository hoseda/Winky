# code Winky interpreter here.


from error import WinkyRuntimeError
from model import *
from state import *
from tokens import *

###################################################################################
#   Constants for runtime value                                                   #
###################################################################################

TYPE_NUMBER = "TYPE_NUMBER" # Integer | Float
TYPE_BOOL   = "TYPE_BOOL"   # True | False
TYPE_String = "TYPE_STRING" # '' | ""



class Interpreter:

    def interpret(self , node , env):
        if isinstance(node , Integer):
            return (TYPE_NUMBER,float(node.value))

        elif isinstance(node , Float):
            return (TYPE_NUMBER,float(node.value))

        elif isinstance(node , Bool):
            return (TYPE_BOOL,node.value)

        elif isinstance(node , String):
            return (TYPE_String,str(node.value))

        elif isinstance(node , Grouping):
            return self.interpret(node.value , env)

        elif isinstance(node , BinOp):
            op_token = node.op.token_type
            lh_type , lhs = self.interpret(node.left , env)
            rh_type , rhs = self.interpret(node.right, env)

            if op_token == TOK_PLUS:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_NUMBER , lhs + rhs)
                elif lh_type == TYPE_String or rh_type == TYPE_String:
                    return (TYPE_String , str(lhs) + str(rhs))
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)
            
            elif op_token == TOK_MINUS:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_NUMBER , lhs - rhs)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)


            elif op_token == TOK_STAR:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_NUMBER , lhs * rhs)
                elif lh_type == TYPE_String and rh_type == TYPE_NUMBER:
                    return (TYPE_String , str(lhs * int(rhs)))
                elif lh_type == TYPE_NUMBER and rh_type == TYPE_String:
                    return (TYPE_String , str(int(lhs) * rhs))
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)

            elif op_token == TOK_SLASH:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    if rhs == 0:
                        WinkyRuntimeError("Division by zero" , node.op.line)
                    return (TYPE_NUMBER , lhs / rhs)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)

            elif op_token == TOK_MOD:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    if rhs == 0:
                        WinkyRuntimeError("Division by zero" , node.op.line)
                    return (TYPE_NUMBER , lhs % rhs)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)

            
            elif op_token == TOK_CARET:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_NUMBER , lhs ** rhs)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)

            elif op_token == TOK_GT:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_BOOL , lhs > rhs)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)

            elif op_token == TOK_LT:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_BOOL , lhs < rhs)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)
            
            elif op_token == TOK_GE:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_BOOL , bool(lhs >= rhs))
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)
            
            elif op_token == TOK_LE:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_BOOL , lhs <= rhs)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)
            
            elif op_token == TOK_EQEQ:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_BOOL , float(lhs) == float(rhs))
                elif lh_type == TYPE_BOOL and rh_type == TYPE_BOOL:
                    return (TYPE_BOOL , lhs == rhs)
                elif lh_type == TYPE_String and rh_type == TYPE_String:
                    return (TYPE_BOOL , str(lhs) == str(rhs))
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)
            
            elif op_token == TOK_NE:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_BOOL , float(lhs) != float(rhs))
                elif lh_type == TYPE_BOOL and rh_type == TYPE_BOOL:
                    return (TYPE_BOOL , lhs != rhs)
                elif lh_type == TYPE_String and rh_type == TYPE_String:
                    return (TYPE_BOOL , str(lhs) != str(rhs))
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)
        
        
        elif isinstance(node , LogicalOp):
            op_token = node.op.token_type
            lh_type , lhs = self.interpret(node.left , env)

            if op_token == TOK_OR:
                if lhs:
                    return (TYPE_BOOL , lhs)
            elif op_token == TOK_AND:
                if not lhs:
                    return (TYPE_BOOL , lhs)
            return self.interpret(node.right , env)

        elif isinstance(node , UnOp):
            operand_token = node.op.token_type
            expr_type , expr = self.interpret(node.value , env)

            if operand_token == TOK_PLUS:
                if expr_type == TYPE_NUMBER:
                    return (TYPE_NUMBER , expr)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} with {expr_type}" , node.op.line)

            elif operand_token == TOK_MINUS:
                if expr_type == TYPE_NUMBER:
                    return (TYPE_NUMBER , -expr)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} with {expr_type}" , node.op.line)

            elif operand_token == TOK_NOT:
                if expr_type == TYPE_BOOL:
                    return (TYPE_BOOL , not expr)
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} with {expr_type}" , node.op.line)
        

        elif isinstance(node , Stmts):
            for stmt in node.stmts:
                self.interpret(stmt , env)


        elif isinstance(node , PrintStmt):
            expr_type , expr_val = self.interpret(node.value , env)
            print(expr_val , end="")

        elif isinstance(node , PrintLnStmt):
            expr_type , expr_val = self.interpret(node.value , env)
            print(expr_val)

        elif isinstance(node , IfStmt):
            test_type , test_val = self.interpret(node.test_expr , env)
            if test_val:
                self.interpret(node.then_stmt , env.new_env()) # inside of the if is a local enviroment
            else:
                if node.else_stmt != None:
                    self.interpret(node.else_stmt , env.new_env())  # inside of the else is a local enviroment
        
        
        elif isinstance(node , Identifier):
            value = env.get_val(node.lexeme)
            if value is None:
                WinkyRuntimeError(f"Undeclared variable {node.lexeme!r}" , node.line)
            if value[1] is None:
                WinkyRuntimeError(f"Uninitialized variable {node.lexeme}" , node.line)
            return value


        elif isinstance(node , Assignment):
            right_type , right_val = self.interpret(node.right , env)
            env.set_val(node.left.lexeme , (right_type , right_val))


    def interpret_ast(self , node):
        '''
        starting function
        '''
        env = Enviroment()
        self.interpret(node , env)
