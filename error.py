# code error handling here.

import sys


def WinkySyntaxError(message , line) -> str:
    print(f"Syntax Error:\n[Line {line} , Message : {message}]")
    sys.exit(1)

def WinkyLexerError(message , row , col) -> str: 
    print(f"Lexer Error:\n[Line {row}:{col} , Message : {message}]")
    sys.exit(1)


    
