import unittest
import inspect

from tokens import *
from lexer import *
from parser import *
from interpreter import *
from utils import *

class TextExpression(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
	    super().__init__(methodName)


    def test_number_primary(self):
        src = '''2.5'''
        expected_result = (TYPE_NUMBER , 2.5)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)
        

    def test_bool_primary(self):
        src = '''false'''
        expected_result = (TYPE_BOOL , False)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)

 
    def test_string_primary(self):
        src = '''"THIS IS STRING"'''
        expected_result = (TYPE_String , "THIS IS STRING")
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)


    def test_addition(self):
        src = '''2 + 4'''
        expected_result = (TYPE_NUMBER , 6)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)
    

    def test_subtracion(self):
        src = '''2 - 5'''
        expected_result = (TYPE_NUMBER , -3)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)

 
    def test_mul(self):
        src = '''2 * 5'''
        expected_result = (TYPE_NUMBER , 10)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)

 
    def test_div(self):
        src = ''' 2 / 5'''
        expected_result = (TYPE_NUMBER , 0.4)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)

 
    def test_percedence(self):
        src = '''2 * 3 + 5'''
        expected_result = (TYPE_NUMBER , 11)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)

    
    def test_unary_minus(self):
        src = '''2 * 9 - -5'''
        expected_result = (TYPE_NUMBER , 23)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)


    def test_caret(self):
        src = '''2^3^2'''
        expected_result = (TYPE_NUMBER , 512)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)

    
    def test_mod(self):
        src = '''4 % 3'''
        expected_result = (TYPE_NUMBER , 1)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)

    
    def test_paren_1(self):
        src = '''2 * (3+9) / 5'''
        expected_result = (TYPE_NUMBER , 4.8)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)


    def test_paren_2(self):
        src = '''2 * (9 + 13) + 2^2 + (((3*3) - 3) + 3.324) / 2.1'''
        expected_result = (TYPE_NUMBER , 52.44)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)


    def test_paren_3(self):
        src = '''14 / (12 / 2) / 2'''
        expected_result = (TYPE_NUMBER , 1.1666666666666667)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)


    def test_bool_or(self):
        src = '''true or false'''
        expected_result = (TYPE_BOOL , True)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)

    
    def test_bool_or_and(self):
        src = '''(44 >= 2) or false and 1 > 0'''
        expected_result = (TYPE_BOOL , True)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)


    def test_not(self):
        src = '''~(44 >= 2)'''
        expected_result = (TYPE_BOOL , False)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)
    

    def test_equal_equal(self):
        src = '''(15 > 3) == ("ali" ~= "Ali")'''
        expected_result = (TYPE_BOOL , True)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)


    def test_not_equal(self):
        src = '''~(3 ~= 2)'''
        expected_result = (TYPE_BOOL , False)
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        res = Interpreter().interpret(ast)
        self.assertEqual(res , expected_result)


if __name__ == "__main__":
    unittest.main()
