# here is the vm.

from hmac import new
from utils import *
from error import *


class Frame:
    def __init__(self , name , ret_pc , fp) -> None:
        self.name = name
        self.ret_pc = ret_pc
        self.fp = fp

class VM:
    def __init__(self) -> None:
        self.stack = []
        self.frames = []
        self.pc = 0
        self.sp = 0
        self.labels = {}
        self.globals = {}
        self.is_running = False


    def generate_label_tabels(self , instruction):
        pc = 0
        for inst in instruction:
            _ , *args = inst
            if _ == "LABEL":
                self.labels.update({args[0] : pc})
            pc +=1

    def push(self, value):
        self.stack.append(value)
        #print(f"NOTIC: {value} WAS PUSHED.")
        self.sp += 1

    def pop(self):
        val = self.stack.pop()
        #print(f"NOTIC: {val} WAS POPED.")
        self.sp -= 1
        return val

    def run(self, instructions):
        self.is_running = True
        
        self.generate_label_tabels(instructions)

        while self.is_running:
            instruction = instructions[self.pc]
            self.pc += 1
            if instruction[0] == "HALT":
                self.is_running = False
                #print("<<-----END OF THE PROGRAM------>>")

            elif instruction[0] == 'LABEL' and instruction[1] == 'START':
                #print("\n<<-----ENTERING START BLOCK----->>")
                pass

            elif instruction[0] == "PUSH":
                val = instruction[1]
                self.push(val)

            else:
                if instruction[0] == "PRINT":
                    val = self.pop()
                    print(stringify(val[1]), end='')

                elif instruction[0] == "PRINTLN":
                    val = self.pop()
                    print(stringify(val[1]), end="\n")

                elif instruction[0] == "ADD":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] + right[1]
                        self.push((TYPE_NUMBER, res))
                    elif left[0] == TYPE_STRING or right[0] == TYPE_STRING:
                        res = stringify(left[1]) + stringify(right[1])
                        self.push((TYPE_STRING, res))
                    else:
                        WinkyVMError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=self.pc - 1)

                elif instruction[0] == "SUB":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] - right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyVMError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=self.pc - 1)

                elif instruction[0] == "MUL":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] * right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyVMError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=self.pc - 1)

                elif instruction[0] == "DIV":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] / right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyVMError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=self.pc - 1)

                elif instruction[0] == "MOD":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] % right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyVMError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=self.pc - 1)

                elif instruction[0] == "EXP":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] ** right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyVMError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=self.pc - 1)
                
                elif instruction[0] == "NEG":
                    val = self.pop()
                    if val[0] == TYPE_NUMBER:
                        res = -val[1]
                        self.push((TYPE_NUMBER , res))
                    else:
                        WinkyVMError(
                            f"Unsupported operator : - and {val[0]}", line=self.pc - 1)
                    
                elif instruction[0] == "AND":
                    right = self.pop()
                    left  = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] & right[1]
                        self.push((TYPE_NUMBER , res))
                    elif left[0] == TYPE_BOOL and right[0] == TYPE_BOOL:
                        res = left[1] & right[1]
                        self.push((TYPE_BOOL , res))
                    else:
                        WinkyVMError(f"Error on {instruction[0]} between {left} and {right}" , line=self.pc - 1)
                
                elif instruction[0] == "OR":
                    right = self.pop()
                    left  = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] | right[1]
                        self.push((TYPE_NUMBER , res))
                    elif left[0] == TYPE_BOOL and right[0] == TYPE_BOOL:
                        res = left[1] | right[1]
                        self.push((TYPE_BOOL , res))
                    else:
                        WinkyVMError(f"Error on {instruction[0]} between {left} and {right}" , line=self.pc - 1)
                
                elif instruction[0] == "XOR":
                    right = self.pop()
                    left  = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] ^ right[1]
                        self.push((TYPE_NUMBER , res))
                    elif left[0] == TYPE_BOOL and right[0] == TYPE_BOOL:
                        res = left[1] ^ right[1]
                        self.push((TYPE_BOOL , res))
                    else:
                        WinkyVMError(f"Error on {instruction[0]} between {left} and {right}" , line=self.pc - 1)
                
                elif instruction[0] == "EQ":
                    right = self.pop()
                    left  = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] == right[1]
                        self.push((TYPE_BOOL , res))
                    elif left[0] == TYPE_BOOL and right[0] == TYPE_BOOL:
                        res = left[1] == right[1]
                        self.push((TYPE_BOOL , res))
                    elif left[0] == TYPE_STRING and right[0] == TYPE_STRING:
                        res = left[1] == right[1]
                        self.push((TYPE_BOOL , res))
                    else:
                        WinkyVMError(f"Error on {instruction[0]} between {left} and {right}" , line=self.pc - 1)
                
                elif instruction[0] == "NE":
                    right = self.pop()
                    left  = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] != right[1]
                        self.push((TYPE_BOOL , res))
                    elif left[0] == TYPE_BOOL and right[0] == TYPE_BOOL:
                        res = left[1] != right[1]
                        self.push((TYPE_BOOL , res))
                    elif left[0] == TYPE_STRING and right[0] == TYPE_STRING:
                        res = left[1] == right[1]
                        self.push((TYPE_BOOL , res))
                    else:
                        WinkyVMError(f"Error on {instruction[0]} between {left} and {right}" , line=self.pc - 1)

                elif instruction[0] == "GT":
                    right = self.pop()
                    left  = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] > right[1]
                        self.push((TYPE_BOOL , res))
                    else:
                        WinkyVMError(f"Error on {instruction[0]} between {left} and {right}" , line=self.pc - 1)
                
                elif instruction[0] == "GE":
                    right = self.pop()
                    left  = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] >= right[1]
                        self.push((TYPE_BOOL , res))
                    else:
                        WinkyVMError(f"Error on {instruction[0]} between {left} and {right}" , line=self.pc - 1)
                
                elif instruction[0] == "LT":
                    right = self.pop()
                    left  = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] < right[1]
                        self.push((TYPE_BOOL , res))
                    else:
                        WinkyVMError(f"Error on {instruction[0]} between {left} and {right}" , line=self.pc - 1)
                
                elif instruction[0] == "LE":
                    right = self.pop()
                    left  = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] <= right[1]
                        self.push((TYPE_BOOL , res))
                    else:
                        WinkyVMError(f"Error on {instruction[0]} between {left} and {right}" , line=self.pc - 1)

                elif instruction[0] == "JMP":
                    self.pc = self.labels[instruction[1]]

                elif instruction[0] == "JMPZ":
                    val_type ,val = self.pop()
                    if val in (0 , False):
                        self.pc = self.labels[instruction[1]]

                elif instruction[0] == "STORE_GLOBAL":
                    self.globals[instruction[1]] = self.pop()
                
                elif instruction[0] == "LOAD_GLOBAL":
                    val = self.globals.get(instruction[1])
                    self.push(val)
                
                elif instruction[0] == "LOAD_LOCAL":
                    val = self.stack[instruction[1]]
                    self.push(val)
                
                elif instruction[0] == "STORE_LOCAL":
                    indx = instruction[1]
                    val = self.pop()
                    self.stack.insert(indx , val)
                
                elif instruction[0] == "SET_LOCAL":
                    pass

                elif instruction[0] == "CALL":
                    new_frame = Frame(instruction[1] , ret_pc=self.pc , fp=self.sp)
                    self.frames.append(new_frame)
                    self.pc = self.labels[instruction[1]]
                
                elif instruction[0] == "RET":
                    self.pc = self.frames[-1].ret_pc
                    self.frames.pop()