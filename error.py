# code error handling here.

import sys


def WinkySyntaxError(message , line) -> str:
    print(f"Syntax Error:\n[Line {line} , Message : {message}]")
    sys.exit(1)

def WinkyLexerError(message , row , col) -> str: 
    print(f"Lexer Error:\n[Line {row}:{col} , Message : {message}]")
    sys.exit(1)


def WinkyRuntimeError(message , line) -> str:
    print(f"RUNTIME ERROR at Line[{line}] , MESSAGE : {message}")
    sys.exit()

