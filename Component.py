class GenericComponent ():
    def update (self):
        raise NotImplementedError("Draw method for " + str(self) + " is not implemented")
    def repr (self):
        return 'GenericComponent'
