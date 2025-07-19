# code utils of winky here.


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


