# here is the vm.

from utils import *
import sys
from error import *

class VM:
    def __init__(self) -> None:
        self.stack = []
        self.pc = 0
    
    def push(self , value):
        self.stack.append(value)
        self.pc += 1
    
    def pop(self):
        val = self.stack.pop()
        self.pc -= 1
        return val

    
    def run(self , instructions):
        for instruction in instructions:
            if instruction[0] == "HALT":
                print("<<-----END OF THE PROGRAM------>>")
                sys.exit(0)

            if instruction[0] == 'LABLE' and instruction[1] == 'START':
                print("\n<<-----ENTERING START BLOCK----->>")

            if instruction[0] == "PUSH":
                val = instruction[1]
                self.push(val)

            else:
                if instruction[0] == "PRINT":
                    val = self.pop()
                    print( stringify(val), end='')

                elif instruction[0] == "PRINTLN":
                    val = self.pop()
                    print(stringify(val) , end="\n")

                elif instruction[0] == "ADD":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] + right[1]
                        self.push(res)
                    elif left[0] == TYPE_STRING or right[0] == TYPE_STRING:
                        res = str(left[1]) + str(right[1])
                        self.push(res)
                    else:
                        WinkyRuntimeError(f"Unsupported operator between {left[0]} and {right[0]}" , line=0)
                    
                
                elif instruction[0] == "SUB":
                    right = self.pop()
                    left = self.pop()
                    res = left - right
                    self.push(res)
                
                elif instruction[0] == "MUL":
                    right = self.pop()
                    left = self.pop()
                    res = left * right
                    self.push(res)
                
                elif instruction[0] == "DIV":
                    right = self.pop()
                    left = self.pop()
                    res = left / right
                    self.push(res)

                elif instruction[0] == "MOD":
                    right = self.pop()
                    left = self.pop()
                    res = left % right
                    self.push(res)

                elif instruction[0] == "EXP":
                    right = self.pop()
                    left = self.pop()
                    res = left ** right
                    self.push(res)




                
            
