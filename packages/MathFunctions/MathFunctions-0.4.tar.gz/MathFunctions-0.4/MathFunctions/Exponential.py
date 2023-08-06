from MathFunctions.Polynomial import Polynomial

factorial = lambda i: 1 if i in [0, 1] else int(i) * factorial(int(i) - 1)
e = 2.7182818284590452353602874713527

class Logarithm(Polynomial):
    def __init__(self, base=e, coef=1, fac=1):
        self.b = base
        super().__init__(arr=[0] + [1 / k for k in range(1, 10000)], coef=coef, freq=fac)
        self.lnb = 1 if abs(base - e) < 1e-8 else Logarithm(base=e)(base)

    __call__ = lambda self, s: 1 if s == self.b else super().__call__((s - 1) / s)


ln, log2, log10 = [Logarithm(base=b) for b in (e, 2, 10)]


class Exponential:
    def __init__(self, base=e, coef=1, fac=1):
        self.b, self.c, self.f = base, coef, fac

    _str__ = lambda self: f'{self.c} * {self.b} ^ ({self.f} * s)'

    __call__ = lambda self, s: self.c * self.b ** (self.f * s)

    integral = lambda self: Exponential(base=self.b, coef=self.c / (self.f * ln(self.b)), fac=self.f)

    derivative = lambda self: Exponential(base=self.b, coef=self.c * (self.f * ln(self.b)), fac=self.f)


exp = Exponential()