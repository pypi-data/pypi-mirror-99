"""Maths related filter function definitions"""
import math
import decimal

from liquid.exceptions import FilterArgumentError

from liquid.filter import Filter
from liquid.filter import expect_integer
from liquid.filter import expect_number


# pylint: disable=arguments-differ too-few-public-methods

D = decimal.Decimal


class MathFilter(Filter):

    __slots__ = ()

    name = "AbstractMathFilter"
    num_args = (0,)
    msg = "{}: expected a number, found {}"

    def __call__(self, val, *args):

        if len(args) not in self.num_args:
            raise FilterArgumentError(
                f"{self.name}: expected {self.num_args} arguments, found {len(args)}"
            )

        num = expect_number(self.name, val)

        try:
            return self.filter(num, *args)
        except (AttributeError, TypeError) as err:
            raise FilterArgumentError(self.msg.format(self.name, type(val))) from err

    def filter(self, val, *args):
        raise NotImplementedError(":(")

    def expect_integer(self, val):
        return expect_integer(self.name, val)

    def expect_number(self, val):
        return expect_number(self.name, val)


class Abs(MathFilter):
    """Return that absolute value of a number.

    Accepts an int, float or a string representations of an int or float.
    """

    __slots__ = ()

    name = "abs"

    def filter(self, num):
        return abs(num)


class AtMost(MathFilter):
    """Return `val` or `args[0]`, whichever is smaller.

    Accepts an int, float or a string representations of an int or float.
    """

    __slots__ = ()

    name = "at_most"
    num_args = (1,)

    def filter(self, num, other):
        other = self.expect_number(other)
        return min(num, other)


class AtLeast(MathFilter):
    """Return `val` or `args[0]`, whichever is greater.

    Accepts an int, float or a string representations of an int or float.
    """

    __slots__ = ()

    name = "at_least"
    num_args = (1,)

    def filter(self, num, other):
        other = self.expect_number(other)
        return max(num, other)


class Ceil(MathFilter):
    """Return the ceiling of x as an Integral.

    Accepts an int, float or a string representations of an int or float.
    """

    __slots__ = ()

    name = "ceil"

    def filter(self, num):
        return math.ceil(num)


class DividedBy(MathFilter):
    """Divide `val` by `args[0]`."""

    __slots__ = ()

    name = "divided_by"
    num_args = (1,)

    def filter(self, num, other):
        other = self.expect_number(other)

        if isinstance(other, float):
            return num / other
        return num // other


class Floor(MathFilter):
    """Return the floor of x as an Integral.

    Accepts an int, float or a string representations of an int or float.
    """

    __slots__ = ()

    name = "floor"

    def filter(self, num):
        return math.floor(num)


class Minus(MathFilter):
    """Subtract one number from another."""

    __slots__ = ()

    name = "minus"
    num_args = (1,)

    def filter(self, num, other):
        other = self.expect_number(other)

        if isinstance(num, float) and isinstance(other, float):
            return float(D(str(num)) - D(str(other)))
        return num - other


class Plus(MathFilter):
    """Add one number to another."""

    __slots__ = ()

    name = "plus"
    num_args = (1,)

    def filter(self, num, other):
        other = self.expect_number(other)

        if isinstance(num, float) and isinstance(other, float):
            return float(D(str(num)) + D(str(other)))
        return num + other


class Round(MathFilter):
    """Round a number to a given precision in decimal digits."""

    __slots__ = ()

    name = "round"
    num_args = (0, 1)

    def filter(self, val, ndigits=None):
        if ndigits:
            ndigits = self.expect_integer(ndigits)
            return round(val, ndigits)
        return round(val)


class Times(MathFilter):
    """Multiply a value by an integer or float."""

    __slots__ = ()

    name = "times"
    num_args = (1,)

    def filter(self, num, other):
        other = self.expect_number(other)

        if isinstance(num, float) and isinstance(other, float):
            return float(D(str(num)) * D(str(other)))
        return num * other


class Modulo(MathFilter):
    """Divide a value by a number and returns the remainder."""

    __slots__ = ()

    name = "modulo"
    num_args = (1,)

    def filter(self, num, other):
        other = self.expect_number(other)

        if isinstance(num, float) and isinstance(other, float):
            return float(D(str(num)) % D(str(other)))
        return num % other
