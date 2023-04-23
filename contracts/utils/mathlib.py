import smartpy as sp  # type: ignore


class Mathlib(sp.Contract):
    def log_2(self, params):
        """
        This function calculates the logarithm base 2 of a positive number with a precision of 20.

        :param params: The input parameter for the logarithm function, which should be a positive number
        """
        sp.verify(params > 0)
        precision = 20
        y = sp.local("y", 0)
        x = sp.local("x", params)
        with sp.while_(x.value < 1 << precision):
            x.value <<= 1
            y.value -= 1 << precision
        with sp.while_(x.value >= 2 << precision):
            x.value >>= 1
            y.value += 1 << precision
        b = sp.local("b", 1 << (precision - 1))
        with sp.while_(0 < b.value):
            x.value = (x.value * x.value) >> precision
            with sp.if_(x.value > 2 << precision):
                x.value >>= 1
                y.value += sp.to_int(b.value)
            b.value >>= 1
        return y.value

    def exp_2(self, x):
        """
        The function returns the result of 2 raised to the power of x using bit shifting.

        :param x: The input parameter x is an integer that represents the exponent of 2. The function
        returns the result of 2 raised to the power of x, which is equivalent to shifting the binary
        representation of 1 by x bits to the left

        :return: The function `exp_2` takes a parameter `x` and returns the result of `1` shifted left
        by `x` bits. In other words, it returns `2` raised to the power of `x`.
        """
        return 1 << x
