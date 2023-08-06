class StepFunction:
    '''
    This class serves to represent and manipulate Macaulay Step MathFunctions programmatically.
    Multiplication and division only work with constants, unlike addition and subtraction.
    '''
    def __init__(self, arr):
        self.ary = [item for item in arr if item[0] != 0] # Removes zeros

    def __add__(self, other):
        arr = self.ary + (other.ary if isinstance(other, StepFunction) else [[other, 0, 0]])
        seen, unique = list(), list()

        for coef, *a in arr: # Simplifies & groups like-terms
            if a not in seen:
                unique.append([coef] + a)
            else:
                c, *_ = unique.pop(seen.index(a))
                seen.remove(a)
                unique.append([c + coef] + a)
            seen.append(a)

        return StepFunction(unique)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            other.c = self * other.c
            return other
        else:
            return StepFunction([[coef*other] + a for coef, *a in self.ary])

    __rsub__ = lambda self, other: self * (-1) + other

    __sub__ = lambda self, other: self + (0 - other)

    __neg__ = lambda self: self * (-1)

    __truediv__ = lambda self, divisor: self * (1 / divisor)

    __call__ = lambda self, x: sum(coef*int(x >= root)*(x - root)**exp for coef, root, exp in self.ary)

    integral = lambda self, C=0: StepFunction([[coef/(exp + 1), root, exp + 1] for coef, root, exp in self.ary]) + C

    derivative = lambda self: StepFunction([[coef * exp, root, exp - 1] for coef, root, exp in self.ary])

    def __iter__(self):
        for elem in self.ary: # So that each term in the function can be accessed as a 'subfunction'
            yield StepFunction([elem])

    @staticmethod
    def optimize(f, a, b): # Uses recursive interval (golden search) minimization
        gold = (1 + 5 ** 0.5) / 2
        beta = 1 / gold
        alpha = 1 - beta
        while abs(b-a) > 1e-8:
            xl = a + alpha*(b-a)
            xr = a + beta*(b-a)
            if f(xl) < f(xr):
                b = xr
            else:
                a = xl
        return round((a + b) / 2, 8)

    argmin = lambda self, a, b: self.optimize(self, a, b)

    argmax = lambda self, a, b: self.optimize((0 - self), a, b) # argmax(f(x)) = argmin(-f(x))

    max = lambda self, a, b: self(self.argmax(a, b))

    min = lambda self, a, b: self(self.argmin(a, b))

    __repr__ = __str__ = lambda self: ' '.join(f"{'+'*int(c>0)}{round(c, 5)}[x{'-'+str(round(r, 2)) if r else ''}]^{e}" for c,r,e in self.ary)

    __rmul__, __radd__ = __mul__, __add__ # Commutative methods