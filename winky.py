#winky compiler code

import sys
from interpreter import Interpreter as INTP
from parser import *
from tokens import *
from lexer import *
from error import *
from vm import *
from compiler import *

DEBUG = False

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Winky 1.0.1 by HOSEDA")
        while(1):
            inp = str(input(">> "))
            if inp == "exit":
                exit()
            tks = Lexer(inp).tokenize()
            ast = Parser(tks).parse()
            INTP().interpret_ast(ast)


    elif len(sys.argv) == 2:

        filename = sys.argv[1]
        print(filename)

        with open(filename) as file:
            source = file.read()
            if len(source) == 0 : WinkyRuntimeError("Source Code is empty" , line=-1)
            tokens = Lexer(source).tokenize()
            ast = Parser(tokens).parse()

            if DEBUG:
        
                print("##################################################################################") 
                print("SOURCE:")
                print(source)

                print("##################################################################################")
                print("LEXER:")
            
                for tok in tokens:
                    print(tok)
        
                print("##################################################################################") 
                print("PARSED AST:")
            
                print(ast)
      
                print("##################################################################################") 
                print("INTERPRETER:")

            
            #intp = INTP()
            #intp.interpret_ast(ast)


            compiler = Compiler()
            code = compiler.compile_code(ast)
            print(code)
            #vm = VM()
            #vm.run(code)


    else:
        raise SystemExit("Usage : python3 winky.py <filename>")
