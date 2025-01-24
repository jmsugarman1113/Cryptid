from __future__ import annotations
from typing import Any
from numbers import Number


# TODO: look at https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/116_complex_fraction/cfrac.py to make this cleaner


class Even(int):
    def __new__(cls, value: int, *args, **kwargs):
        if not isinstance(value, int) and value % 2 != 0:
            raise ValueError("Even type must be even")
        return super(cls, cls).__new__(cls, value)

    def __add__(self, other: Any) -> Number:
        res = super(Even, self).__add__(other)
        if res % 2 == 0:
            return self.__class__(res)
        return res

    def __sub__(self, other: Any) -> Number:
        res = super(Even, self).__sub__(other)
        if res % 2 == 0:
            return self.__class__(res)
        return res

    def __mul__(self, other: Any) -> Number:
        res = super(Even, self).__mul__(other)
        if isinstance(other, int):
            return self.__class__(res)
        return res

    def __div__(self, other: Any) -> Number:
        res = super(Even, self).__div__(other)
        if isinstance(res, int) and res % 2 == 0:
            return self.__class__(res)
        return res

    def __truediv__(self, other: Any) -> Number:
        res = super(Even, self).__truediv__(other)
        if isinstance(res, int) and res % 2 == 0:
            return self.__class__(res)
        return res

    def __repr__(self) -> str:
        return f"Even({int(self)})"
