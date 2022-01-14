# -*- coding: utf-8 -*-

# Built-in imports
import base64
import pathlib

# Imports from own package/module
from src.tkcalculator.icon import ICON
from src.tkcalculator.config import DATA


class Util:

    @staticmethod
    def get_iconphoto(filepath=None):
        if isinstance(filepath, str):
            path = pathlib.Path(filepath)
            if all([path.is_file(), path.suffix == '.png']):
                return path.read_bytes()
        return base64.urlsafe_b64decode(ICON)

    @staticmethod
    def select_config(name='defaults'):
        name = 'default' if name not in DATA.keys() else name
        return DATA[name]

    @staticmethod
    def get_config_list():
        return list(DATA.keys())

    class Calculator(object):
        """Process the string given from the expression parameter.
        If the string is a valid Arithmetic expression then return
        the result from Python's built-in eval() method. Otherwise,
        return an "Error" string like an actual calculator.

        Python's eval() is a very useful tool, the function has some
        important security implications to consider before using.
        """

        def __init__(self, expression: str):

            if isinstance(expression, str):
                self.expression = expression
                self.result = self.calculate_equation(self.expression)

            # Raise a TypeError if argument is not a str
            else:
                exception = TypeError("must be str, not %s" % expression)
                raise exception

        @staticmethod
        def calculate_equation(expression: str) -> str:
            """Return the value from the evaluation of the given
            expression as a string. Otherwise, return "Error".
            """
            try:
                output = eval(expression)

                # Format the output to give a slightly better or accurate result
                if isinstance(output, float):

                    if str(output).endswith('.0'):
                        output = int(output)

                    elif str(output).count('0') > 5:
                        output = str(round(output, 8))
                        # Temporary bugfix in the likes of expression "2500*0.17"
                        output = Util.Calculator.calculate_equation(output)

            except (BaseException, Exception):
                output = "Error"

            return str(output)

        @staticmethod
        def div_percentage(number, percentage):
            """Dividing a number by a percentage of itself"""
            # Discourages negative inputs
            if not number < 0 or percentage < 0:
                return number / (percentage / 100)

        @staticmethod
        def mul_percentage(number, percentage):
            """Multiplying a number by a percentage of itself"""
            # Discourages negative inputs
            if not number < 0 or percentage < 0:
                return number * (percentage / 100)

        @staticmethod
        def add_percentagee(number, percentage):
            """Adding a number by a percentage of itself"""
            # Discourages negative inputs
            if not number < 0 or percentage < 0:
                n = Util.Calculator.mul_percentage(number, percentage)
                return number + n

        @staticmethod
        def sub_percentagee(number, percentage):
            """Adding a number by a percentage of itself"""
            # Discourages negative inputs
            if not number < 0 or percentage < 0:
                n = Util.Calculator.mul_percentage(number, percentage)
                return number - n
