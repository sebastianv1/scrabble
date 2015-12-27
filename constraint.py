
class Constraint:
    def __init__(self, x, y, domain, tile_val=None):
        self.x = x
        self.y = y
        self.h_domain = domain[:]
        self.v_domain = domain[:]
        self.tile = tile_val
    
    def removeValueFromDomain(self, val, horizontal=True):
        if horizontal:
            self.h_domain.remove(val)
        else:
            self.v_domain.remove(val)
    def __repr__(self):
        string = "(" + str(self.x) + "," + str(self.y) + ")\n"
        string += "H_Domain: " + str(self.h_domain)
        return string
