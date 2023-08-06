from MathFunctions.Polynomial import Polynomial

class Sin(Polynomial):
    '''
    Sine Function from its Taylor Series
    '''

    def __init__(self, freq=1, coef=1):
        factorial = lambda i: 1 if i in [0, 1] else int(i) * factorial(int(i) - 1)

        super().__init__([0 if not i % 2 else (-1) ** (i // 2) / factorial(i) for i in range(100)], freq, coef)

    __str__ = lambda self: f'{self.c}Sin({self.f}s)'

    __call__ = lambda self, s: super().__call__(((self.f * s) % (3.141592653589793 * 2)) / self.f)

    integral = lambda self, C=0: Cos(self.f, -self.c / self.f)

    derivative = lambda self: Cos(self.f, self.c * self.f)


class Cos(Polynomial):
    '''
    Cosine Function from its Taylor Series
    '''

    def __init__(self, freq=1, coef=1):
        factorial = lambda i: 1 if i in [0, 1] else int(i) * factorial(int(i) - 1)

        super().__init__([0 if i % 2 else (-1) ** (i // 2) / factorial(i) for i in range(100)], freq, coef)

    __str__ = lambda self: f'{self.c}Cos({self.f}s)'

    __call__ = lambda self, s: super().__call__(((self.f * s) % (3.141592653589793 * 2)) / self.f)

    integral = lambda self, C=0: Sin(self.f, self.c / self.f)

    derivative = lambda self: Sin(self.f, -self.c * self.f)


cos, sin = Cos(), Sin()
tan = lambda s: sin(s) / cos(s)