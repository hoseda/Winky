# here is the vm.

from utils import *
import sys
from error import *


class VM:
    def __init__(self) -> None:
        self.stack = []
        self.pc = 0
        self.sp = 0
        self.is_running = False

    def push(self, value):
        self.stack.append(value)
        print(f"NOTIC: {value} WAS PUSHED.")
        self.sp += 1

    def pop(self):
        val = self.stack.pop()
        print(f"NOTIC: {val} WAS POPED.")
        self.sp -= 1
        return val

    def run(self, instructions):
        self.is_running = True
        while self.is_running:
            instruction = instructions[self.pc]
            self.pc += 1
            if instruction[0] == "HALT":
                self.is_running = False
                print("<<-----END OF THE PROGRAM------>>")

            elif instruction[0] == 'LABLE' and instruction[1] == 'START':
                print("\n<<-----ENTERING START BLOCK----->>")

            elif instruction[0] == "PUSH":
                val = instruction[1]
                self.push(val)

            else:
                if instruction[0] == "PRINT":
                    val = self.pop()
                    print(stringify(val), end='')

                elif instruction[0] == "PRINTLN":
                    val = self.pop()
                    print(stringify(val), end="\n")

                elif instruction[0] == "ADD":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] + right[1]
                        self.push((TYPE_NUMBER, res))
                    elif left[0] == TYPE_STRING or right[0] == TYPE_STRING:
                        res = str(left[1]) + str(right[1])
                        self.push((TYPE_STRING, res))
                    else:
                        WinkyRuntimeError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=0)

                elif instruction[0] == "SUB":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] - right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyRuntimeError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=0)

                elif instruction[0] == "MUL":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] * right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyRuntimeError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=0)

                elif instruction[0] == "DIV":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] / right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyRuntimeError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=0)

                elif instruction[0] == "MOD":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] % right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyRuntimeError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=0)

                elif instruction[0] == "EXP":
                    right = self.pop()
                    left = self.pop()
                    if left[0] == TYPE_NUMBER and right[0] == TYPE_NUMBER:
                        res = left[1] ** right[1]
                        self.push((TYPE_NUMBER, res))
                    else:
                        WinkyRuntimeError(
                            f"Unsupported operator between {left[0]} and {right[0]}", line=0)
                
                elif instruction[0] == "NEG":
                    val = self.pop()
                    if val[0] == TYPE_NUMBER:
                        res = -val[1]
                        self.push((TYPE_NUMBER , res))
                    else:
                        WinkyRuntimeError(
                            f"Unsupported operator : - and {val[0]}", line=0)
