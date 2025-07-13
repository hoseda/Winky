#winky compiler code

import sys
from interpreter import Interpreter as INTP
from parser import *
from tokens import *
from lexer import *

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Winky 1.0.1 by HOSEDA")
        while(1):
            inp = str(input(">> "))
            if inp == "exit":
                exit()
            tks = Lexer(inp).tokenize()
            ast = Parser(tks).parse()
            intp = INTP().interpret(ast)


    elif len(sys.argv) == 2:

        filename = sys.argv[1]
        print(filename)

        with open(filename) as file:
            source = file.read()
        
            print("##################################################################################") 
            print("SOURCE:")
            print(source)

            print("##################################################################################")
            print("LEXER:")
            tokens = Lexer(source).tokenize()
            for tok in tokens:
                print(tok)
        
            print("##################################################################################") 
            print("PARSED AST:")
            ast = Parser(tokens).parse()
            print(ast)
      
            print("##################################################################################") 
            print("INTERPRETER:")
            intp = INTP()
            intp.interpret(ast)

    else:
        raise SystemExit("Usage : python3 winky.py <filename>")
