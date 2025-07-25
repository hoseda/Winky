# code Winky interpreter here.


from error import WinkyRuntimeError
from model import *
from state import *
from tokens import *
from utils import *
import codecs


class Interpreter:

    def interpret(self , node , env):
        if isinstance(node , Integer):
            return (TYPE_NUMBER,float(node.value))

        elif isinstance(node , Float):
            return (TYPE_NUMBER,float(node.value))

        elif isinstance(node , Bool):
            return (TYPE_BOOL,node.value)

        elif isinstance(node , String):
            return (TYPE_STRING,str(node.value))

        elif isinstance(node , Grouping):
            return self.interpret(node.value , env)

        elif isinstance(node , BinOp):
            op_token = node.op.token_type
            lh_type , lhs = self.interpret(node.left , env)
            rh_type , rhs = self.interpret(node.right, env)

            if op_token == TOK_PLUS:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_NUMBER , lhs + rhs)
                elif lh_type == TYPE_STRING or rh_type == TYPE_STRING:
                    return (TYPE_STRING , stringify(lhs) + stringify(rhs))
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
                elif lh_type == TYPE_STRING and rh_type == TYPE_NUMBER:
                    return (TYPE_STRING , str(lhs * int(rhs)))
                elif lh_type == TYPE_NUMBER and rh_type == TYPE_STRING:
                    return (TYPE_STRING , str(int(lhs) * rhs))
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
                elif lh_type == TYPE_STRING and rh_type == TYPE_STRING:
                    return (TYPE_BOOL , str(lhs) == str(rhs))
                else:
                    WinkyRuntimeError(f"Unsupported operator {node.op.lexeme!r} between {lh_type} and {rh_type}" , node.op.line)
            
            elif op_token == TOK_NE:
                if lh_type == TYPE_NUMBER and rh_type == TYPE_NUMBER:
                    return (TYPE_BOOL , float(lhs) != float(rhs))
                elif lh_type == TYPE_BOOL and rh_type == TYPE_BOOL:
                    return (TYPE_BOOL , lhs != rhs)
                elif lh_type == TYPE_STRING and rh_type == TYPE_STRING:
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
            print(codecs.escape_decode(bytes(stringify(expr_val),"utf-8"))[0].decode("utf-8") , end=node.end)


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
        
            
        elif isinstance(node , LocalAssignment):
            right_type , right_val = self.interpret(node.right , env)
            env.set_local(node.left.lexeme , (right_type , right_val))

        
        elif isinstance(node , WhileStmt):
            while self.interpret(node.test_expr , env)[1]:
                self.interpret(node.while_stmts , env.new_env())


        elif isinstance(node , ForStmt):
            identifier = node.identifier.lexeme
            start_type , start_val = self.interpret(node.start_expr , env)
            end_type , end_val  = self.interpret(node.end_expr , env)
            new_env = env.new_env()
            if start_val < end_val:
                if node.stepper_expr is None:
                    step_val = 1
                else:
                    step_type , step_val = self.interpret(node.stepper_expr , env)
                while start_val <= end_val:
                    newval = (TYPE_NUMBER , start_val)
                    new_env.set_val(identifier , newval)
                    self.interpret(node.for_stmts , new_env)
                    start_val = start_val + step_val
                
            else:
                if node.stepper_expr is None:
                    step_val = -1
                else:
                    step_type , step_val = self.interpret(node.stepper_expr, env)
   
                while start_val >= end_val:
                    newval = (TYPE_NUMBER , start_val)
                    new_env.set_val(identifier , newval)
                    self.interpret(node.for_stmts , new_env)
                    start_val = start_val + step_val


        elif isinstance(node , FuncDecl):
            env.set_func(node.name , node.params , node.body_stmts , env)

    
        elif isinstance(node , FuncCall):
            func = env.get_func(node.name)
 
            if func is None:
                WinkyRuntimeError(f"Undefined Function {node.name}" , line=node.line)

            elif len(func[0]) != len(node.args):
                WinkyRuntimeError(f"Unexpected argument , Function {node.name} needs {len(func[0])} arguments but there is {len(node.args)} here." , line=node.line)

            else:
                # create a new enviroment for local variable.
                new_env = func[2].new_env()
                # set values of params assigns with args
                for param , arg in zip(func[0] , node.args):
                    new_env.set_local(param.name , self.interpret(arg , env)) 
                
                try:    
                    self.interpret(func[1] , new_env) 
                except Return as e:
                    return e.args[0]

        elif isinstance(node , FuncCallStmt):
            self.interpret(node.expr , env)

        
        elif isinstance(node , RetStmt):
            raise Return(self.interpret(node.expr , env))



    def interpret_ast(self , node):
        '''
        starting function
        '''
        env = Enviroment()
        self.interpret(node , env)


class Return(Exception):
    pass