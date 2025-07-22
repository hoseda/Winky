# code utils of winky here.

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
        if i[0] == 'LABLE':
            print(f"{i[1]}:")
        elif i[0] == 'PUSH':
            print(f"    PUSH {stringify(i[1][1])}")
        else:
            print(f"    {i[0]}")
