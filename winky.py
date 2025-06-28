#winky compiler code

import sys
from parser import *
from tokens import *
from lexer import *

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage : python3 winky.py <filename>")

    filename = sys.argv[1]
    print(filename)

    with open(filename) as file:
        source = file.read()
        
        print("##################################################################################")
        print("LEXER:")
        
        tokens = Lexer(source).tokenize()
        
        for tok in tokens:
            print(tok)
        
        print("PARSED AST:")
        ast = Parser(tokens).parse()

        print("##################################################################################")
        print(ast)
        
