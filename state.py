# code enviroment here.


from os import set_inheritable


class Enviroment():
    def __init__(self , parent=None):
        self.vars = {}  # store variables here.
        self.parent = parent

    def get_val(self , name):
        while self:
            val = self.vars.get(name)
            if val is not None:
                return val
            else:
                self = self.parent
        return None


    def set_val(self , name , value):
        original_slef = self

        while self:
            if name in self.vars:
                self.vars[name] = value
                return value
            self = self.parent
        original_slef.vars[name] = value

    def new_env(self):
        '''
        creating a nested child enviroment and the parent is this current enviroment.
        '''
        return Enviroment(parent=self)

