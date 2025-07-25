# code utils of winky here.

from dis import Instruction
from operator import le


TYPE_NUMBER = "TYPE_NUMBER"
TYPE_STRING = "TYPE_STRING"
TYPE_BOOL   = "TYPE_BOOL"


def prettyPrint(ast):
    # this function here will use to print ast pretty.
    pass



class Colors:
    # this class will use as a constant of ANSII sequence character for colorizing the printing text, error,..etc
    pass




def stringify(val):
    if isinstance(val , bool):
        if val:
            return "true"
        else:
            return "false"

    if isinstance(val , float) and val.is_integer():
        return str(int(val))
    
    return str(val)




def formatting_code_generation(code : list):
    for i  in code:
        if i[0] == 'LABEL':
            print(f"{i[1]}:")
            continue
        if i[0] == "PUSH":
            print(f"    {i[0]} {stringify(i[1][1])}")
        elif len(i) == 1:
            print(f"    {stringify(i[0])}")
            continue
        elif len(i) == 2:
            print(f"    {stringify(i[0])} {stringify(i[1])}")
            continue
        else:
            print(f"    {i[0]}")
