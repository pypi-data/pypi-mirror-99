class Polynomial:
    '''
    This class serves to represent and manipulate Polynomial Functions programmatically.
    Multiplication and division only work with constants, unlike addition and subtraction.
    '''
    def __init__(self, arr, freq=1, coef=1):
        self.ary, self.f, self.c = arr, freq, coef

    def __add__(self, other):
        if isinstance(other, Polynomial):
            arr = [self.c*i*self.f**o + other.c*j*other.f**o for o, (i, j) in enumerate(zip(self.ary, other.ary))]
        else:
            arr = [self.ary[0] + other / self.c] + self.ary[1:]
        return Polynomial(arr)

    def __mul__(self, other):
        self.c *= other
        return self

    __rsub__ = lambda self, other: other + self * (-1)

    __sub__ = lambda self, other: self + (0 - other)

    __neg__ = lambda self: self * (-1)

    __truediv__ = lambda self, divisor: self * (1 / divisor)

    __call__ = lambda self, s: self.c * sum(ci * (self.f * s) ** i for i, ci in enumerate(self.ary))

    integral = lambda self, C=0: Polynomial([C*self.f/self.c] + [ci/(i+1) for i, ci in enumerate(self.ary)], self.f, self.c / self.f)

    dintegral = lambda self, a, b: self.integral()(b) - self.integral()(a)

    derivative = lambda self: Polynomial([ci * (i + 1) for i, ci in enumerate(self.ary[1:])], self.f, self.c * self.f)

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

    __str__ = lambda self: str(self.c) + '(' + ' + '.join(f"{c}s^{e}" for e, c in enumerate(self.ary) if c) + ')'

    __rmul__, __radd__ = __mul__, __add__ # Commutative methods

class Linear(Polynomial):
    '''
    Linear MathFunctions of form y=mx + b
    '''
    def __init__(self, m=1, b=0):
        super().__init__([b, m], 1, 1)
        self.m, self.b = m, b

    __str__ = lambda self: f'{self.m}s + {self.b}'