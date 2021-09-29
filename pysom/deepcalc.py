from .components.calc import Calculator
from .utils.add import add
from .utils.subtract import subtract
from .utils.multiply import multiply
from .utils.divide import divide


class DeepCalculator():
    def __init__(self):
        """
        Doesn't do anything useful at this point in time.
        """
        pass

    def do_random(self) -> None:
        """
        Does a bunch of random operations.
        """
        a_calc = Calculator(add)
        s_calc = Calculator(subtract)
        m_calc = Calculator(multiply)
        d_calc = Calculator(divide)

        print(a_calc)
        print(a_calc.do(5.0, 3.0))

        # Let's try chaining calculations aka "deep calc" lol
        res = a_calc.do(2, s_calc.do(12, m_calc.do(2, d_calc.do(50, 25))))
        print(res)

        return None


if __name__ == "__main__":
    dc = DeepCalculator()
    dc.do_random()
