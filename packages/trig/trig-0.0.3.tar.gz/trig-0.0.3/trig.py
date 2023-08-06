"""
Trig provides many trigonometric functions.

There are two behaviours for each function, depending on the type of the
argument. With a float (or int) argument, a float is returned if
possible, otherwise the result will be a complex. With a complex
argument, a complex is always returned.
"""
from __future__ import annotations

import cmath
import functools
from typing import Union


def handle_complex(function):
    function.__annotations__ = {"x": complex, "return": Union[float, complex]}

    @functools.wraps(function)
    def new(x):
        y = function(x)
        if isinstance(x, complex):
            return y
        return y if y.imag else y.real

    return new


@handle_complex
def sin(x):
    """Return the sine of x."""
    return cmath.sin(x)


@handle_complex
def asin(x):
    """Return the arcsine of x."""
    return cmath.asin(x)


@handle_complex
def cos(x):
    """Return the cosine of x."""
    return cmath.cos(x)


@handle_complex
def acos(x):
    """Return the arccosine of x."""
    return cmath.acos(x)


@handle_complex
def tan(x):
    """Return the tangent of x."""
    return cmath.tan(x)


@handle_complex
def atan(x):
    """Return the arctangent of x."""
    return cmath.atan(x)


@handle_complex
def sec(x):
    """Return the secant of x."""
    return 1 / cmath.cos(x)


@handle_complex
def asec(x):
    """Return the arcsecant of x."""
    y = cmath.acos(1 / x)
    if y.real < 0:
        return y + cmath.tau
    return y


@handle_complex
def csc(x):
    """Return the cosecant of x."""
    return 1 / cmath.sin(x)


@handle_complex
def acsc(x):
    """Return the arccosecant of x."""
    return cmath.asin(1 / x)


@handle_complex
def cot(x):
    """Return the cotangent of x."""
    return 1 / cmath.tan(x)


@handle_complex
def acot(x):
    """Return the arccotangent of x."""
    return cmath.pi / 2 - cmath.atan(x)


@handle_complex
def ver(x):
    """Return the versine of x."""
    return 1 - cmath.cos(x)


@handle_complex
def aver(x):
    """Return the arcversine of x."""
    return cmath.acos(1 - x)


@handle_complex
def cvs(x):
    """Return the coversine of x."""
    return 1 - cmath.sin(x)


@handle_complex
def acvs(x):
    """Return the arccoversine of x."""
    return cmath.asin(1 - x)


@handle_complex
def vcs(x):
    """Return the vercosine of x."""
    return 1 + cmath.cos(x)


@handle_complex
def avcs(x):
    """Return the arcvercosine of x."""
    return cmath.acos(x - 1)


@handle_complex
def cvc(x):
    """Return the covercosine of x."""
    return 1 + cmath.sin(x)


@handle_complex
def acvc(x):
    """Return the arccovercosine of x."""
    return cmath.asin(x - 1)


@handle_complex
def hvs(x):
    """Return the haversine of x."""
    return (1 - cmath.cos(x)) / 2


@handle_complex
def ahvs(x):
    """Return the archaversine of x."""
    return cmath.acos(1 - 2 * x)


@handle_complex
def hcv(x):
    """Return the hacoversine of x."""
    return (1 - cmath.sin(x)) / 2


@handle_complex
def ahcv(x):
    """Return the archacoversine of x."""
    return cmath.asin(1 - 2 * x)


@handle_complex
def hvc(x):
    """Return the havercosine of x."""
    return (1 + cmath.cos(x)) / 2


@handle_complex
def ahvc(x):
    """Return the archavercosine of x."""
    return cmath.acos(2 * x - 1)


@handle_complex
def hcc(x):
    """Return the hacovercosine of x."""
    return (1 + cmath.sin(x)) / 2


@handle_complex
def ahcc(x):
    """Return the archacovercosine of x."""
    return cmath.asin(2 * x - 1)


@handle_complex
def exs(x):
    """Return the exsecant of x."""
    return 1 / cmath.cos(x) - 1


@handle_complex
def aexs(x):
    """Return the arcexsecant of x."""
    return cmath.acos(1 / (x + 1))


@handle_complex
def exc(x):
    """Return the excosecant of x."""
    return 1 / cmath.sin(x) - 1


@handle_complex
def aexc(x):
    """Return the arcexcosecant of x."""
    return cmath.asin(1 / (x + 1))


@handle_complex
def crd(x):
    """Return the chord of x."""
    return 2 * cmath.sin(x / 2)


@handle_complex
def acrd(x):
    """Return the arcchord of x."""
    return cmath.asin(x / 2) * 2


@handle_complex
def sinh(x):
    """Return the hyperbolic sine of x."""
    return cmath.sinh(x)


@handle_complex
def asinh(x):
    """Return the hyperbolic arsine of x."""
    return cmath.asinh(x)


@handle_complex
def cosh(x):
    """Return the hyperbolic cosine of x."""
    return cmath.cosh(x)


@handle_complex
def acosh(x):
    """Return the hyperbolic arcosine of x."""
    return cmath.acosh(x)


@handle_complex
def tanh(x):
    """Return the hyperbolic tangent of x."""
    return cmath.tanh(x)


@handle_complex
def atanh(x):
    """Return the hyperbolic artangent of x."""
    return cmath.atanh(x)


@handle_complex
def sech(x):
    """Return the hyperbolic secant of x."""
    return 1 / cmath.cosh(x)


@handle_complex
def asech(x):
    """Return the hyperbolic arsecant of x."""
    return cmath.acosh(1 / x)


@handle_complex
def csch(x):
    """Return the hyperbolic cosecant of x."""
    return 1 / cmath.sinh(x)


@handle_complex
def acsch(x):
    """Return the hyperbolic arcosecant of x."""
    return cmath.asinh(1 / x)


@handle_complex
def coth(x):
    """Return the hyperbolic cotangent of x."""
    return 1 / cmath.tanh(x)


@handle_complex
def acoth(x):
    """Return the hyperbolic arcotangent of x."""
    return cmath.atanh(1 / x)


@handle_complex
def verh(x):
    """Return the hyperbolic versine of x."""
    return 1 - cmath.cosh(x)


@handle_complex
def averh(x):
    """Return the hyperbolic arversine of x."""
    return cmath.acosh(1 - x)


@handle_complex
def cvsh(x):
    """Return the hyperbolic coversine of x."""
    return 1 - cmath.sinh(x)


@handle_complex
def acvsh(x):
    """Return the hyperbolic arcoversine of x."""
    return cmath.asinh(1 - x)


@handle_complex
def vcsh(x):
    """Return the hyperbolic vercosine of x."""
    return 1 + cmath.cosh(x)


@handle_complex
def avcsh(x):
    """Return the hyperbolic arvercosine of x."""
    return cmath.acosh(x - 1)


@handle_complex
def cvch(x):
    """Return the hyperbolic covercosine of x."""
    return 1 + cmath.sinh(x)


@handle_complex
def acvch(x):
    """Return the hyperbolic arcovercosine of x."""
    return cmath.asinh(x - 1)


@handle_complex
def hvsh(x):
    """Return the hyperbolic haversine of x."""
    return (1 - cmath.cosh(x)) / 2


@handle_complex
def ahvsh(x):
    """Return the hyperbolic arhaversine of x."""
    return cmath.acosh(1 - 2 * x)


@handle_complex
def hcvh(x):
    """Return the hyperbolic hacoversine of x."""
    return (1 - cmath.sinh(x)) / 2


@handle_complex
def ahcvh(x):
    """Return the hyperbolic arhacoversine of x."""
    return cmath.asinh(1 - 2 * x)


@handle_complex
def hvch(x):
    """Return the hyperbolic havercosine of x."""
    return (1 + cmath.cosh(x)) / 2


@handle_complex
def ahvch(x):
    """Return the hyperbolic arhavercosine of x."""
    return cmath.acosh(2 * x - 1)


@handle_complex
def hcch(x):
    """Return the hyperbolic hacovercosine of x."""
    return (1 + cmath.sinh(x)) / 2


@handle_complex
def ahcch(x):
    """Return the hyperbolic arhacovercosine of x."""
    return cmath.asinh(2 * x - 1)


@handle_complex
def exsh(x):
    """Return the hyperbolic exsecant of x."""
    return 1 / cmath.cosh(x) - 1


@handle_complex
def aexsh(x):
    """Return the hyperbolic arexsecant of x."""
    return cmath.acosh(1 / (x + 1))


@handle_complex
def exch(x):
    """Return the hyperbolic excosecant of x."""
    return 1 / cmath.sinh(x) - 1


@handle_complex
def aexch(x):
    """Return the hyperbolic arexcosecant of x."""
    return cmath.asinh(1 / (x + 1))


@handle_complex
def crdh(x):
    """Return the hyperbolic chord of x."""
    return (1 - cmath.exp(-x)) * ((cmath.exp(2 * x) + 1) / 2) ** 0.5


@handle_complex
def acrdh(x):
    """Return the hyperbolic archord of x."""
    m = cmath.sqrt(2 * x ** 2 + 1)

    v = cmath.log((1 + m + cmath.sqrt(2 * (x ** 2 + m - 1))) / 2)
    if x.real < 0 or x.real == 0 and x.imag < 0:
        return -v
    return v
