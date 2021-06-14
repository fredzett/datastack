import numpy as np

class V:
    def __init__(self, *vs):
        self._vs = np.array(vs)

    def __repr__(self):
        s = "["
        s += ", ".join([str(v) for v in self._vs])
        s += "]"
        return s


    def __mul__(self,other):
        if type(other) in [int, float, np.ndarray]:
            res = self._vs * other
            return V(*res)
        elif isinstance(other, V):
            res = self._vs * other._vs
            return V(*res)
        else:
            raise NotImplementedError(f"Multiplication with type '{type(other)}' not possible")

    __rmul__ = __mul__
        

