from typing import Callable


class Calculator:
    def __init__(self, func: Callable[[float, float], float]):
        """
        A simple calculator class that can be layered onto the
        DeepCalculator class. Can load basic functionality from the utilities
        module.

        Args:
            func (Callable[[float, float], float]): the operation to be loaded
        """
        self.func = func

    def do(self, arg1: float, arg2: float) -> float:
        """
        Wrapper functionality to allow the calculator functionality to be
        called by name. For example, calc.do(add) can be used instead of
        calc.funcs.add()

        Args:
            arg1 (float): the first operand
            arg2 (float): the second operand

        Returns:
            float: the result
        """
        return self.func(arg1, arg2)

    def __str__(self) -> str:
        """
        Returns string interpretation of the Calculator class.
        Lists all modules added to the calculator

        Returns:
            str: a string interpretation of the Calculator
        """
        msg = "Hello, I am a calculator, loaded with " + \
            "the following feature: '{}'".format(self.func.__name__)

        return msg
