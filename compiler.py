# code compier here.
# compiler generate the byte-code assocaited to souce code


from model import *
from tokens import *
from utils import *
from error import *

class Symbol:
    def __init__(self , name) -> None:
        self.name = name
    
    def __repr__(self) -> str:
        return f"Symbol({self.name})"

class Compiler:
    def __init__(self) -> None:
        self.code = []
        self.globals = []
        self.num_globals = 0
        self.lbli = 0

    def emit(self , instruction : tuple):
        self.code.append(instruction)

    def make_label(self):
        lbl = f"LBL{self.lbli}"  
        self.lbli += 1
        return lbl
    
    def get_symbol(self , name):
        for symbol in self.globals:
            if name == symbol.name:
                return symbol
            
        return None
    
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
                self.emit(("PUSH" , (TYPE_BOOL, True)))
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

        # if statement is like this :
        ##  if <test> then
        ##      <then_block>
        ##  else
        ##      <else_block>
        # and in byte-code or assembly its like this :
        ##  IF not <test> JMP L1
        ##  <then_block>
        ##  ....
        ##  JMP L2
        ##  L1:
        ##      <else_block>
        ##      ....
        ##  L2:
        # so here we should act like this :
        # 1) compile the test expression.
        # 2) make labels for then blok , else block and exit.
        # 3) first thing to emit is ("JMPZ" , else_label). the meaning is if test_expr is ZERO/FALSE jump to else_lable and  run the code in there.
        # 4) next one to emit is ("LABEL" , then_label). the meaning is if we didn't jump to else_label then we have to run the code in then_label.
        #    we also compile the code in it.
        # 5) after compiling the code in then_label we should jump to exit_label , and also we emit the else label to chunk of code but only if 
        #    there is an else block , we compile code in that block too.
        # 6) in the end we emit the exit_label.
        elif isinstance(node , IfStmt):
            self.compile(node.test_expr)

            then_label = self.make_label()
            else_label = self.make_label()
            exit_label = self.make_label()
            
            self.emit(("JMPZ" , else_label))

            self.emit(("LABEL" , then_label))
            self.compile(node.then_stmt)

            self.emit(("JMP" , exit_label))
            self.emit(("LABEL" , else_label))

            if node.else_stmt:
                self.compile(node.else_stmt)
            
            self.emit(("LABEL" , exit_label))

        elif isinstance(node , Assignment):
            self.compile(node.right)
            symbol = self.get_symbol(node.left.lexeme)

            if not symbol:
                new_symbol = Symbol(node.left.lexeme)
                self.globals.append(new_symbol)
                self.emit(("STORE_GLOBAL" , new_symbol.name))
                self.num_globals += 1
            else:
                self.emit(("STORE_GLOBAL" , symbol.name))

        elif isinstance(node , Identifier):
            symbol = self.get_symbol(node.lexeme)
            if not symbol:
                WinkyCompileError(f"Undeclared Identifier {node.lexeme}" , line=node.line)
            else:
                self.emit(("LOAD_GLOBAL" , symbol.name))

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
        self.emit(("LABEL" , "START"))
        self.compile(node)
        self.emit(("HALT",))
        return self.code
