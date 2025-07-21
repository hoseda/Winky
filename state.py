# code enviroment here.


class Enviroment():
    def __init__(self , parent=None):
        self.vars = {}  # store variables here.
        self.funcs = {} # store functions here.
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


    def get_func(self,name):
        while self:
            val = self.funcs.get(name)
            if val is not None:
                return val
            else:
                self = self.parent
        return None

    
    def set_func(self, name  , args , body , env):
        value = (args , body , env)
        self.funcs[name] = value
    
    def new_env(self):
        '''
        creating a nested child enviroment and the parent is this current enviroment.
        '''
        return Enviroment(parent=self)


    def __repr__(self) -> str:
        return f"Enviroment(Vars: [{self.vars}] , Funcs: [{self.funcs}])"


