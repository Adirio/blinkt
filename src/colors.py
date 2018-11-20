"""
MIT License

Copyright (c) 2018 Adrián

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import colorsys


BIT_DEPTH = 255


class Color:
    __slots__ = ('_r', '_g', '_b')

    def __init__(self, r: int=0, g: int=0, b: int=0) -> None:
        self._r = BIT_DEPTH if r >= BIT_DEPTH else 0 if r <= 0 else r
        self._g = BIT_DEPTH if g >= BIT_DEPTH else 0 if g <= 0 else g
        self._b = BIT_DEPTH if b >= BIT_DEPTH else 0 if b <= 0 else b

    @classmethod
    def rgb(cls, r: float=0.0, g: float=0.0, b: float=0.0) -> "Color":
        # Check boundaries
        r = 1.0 if r >= 1.0 else 0.0 if r <= 0.0 else r
        g = 1.0 if g >= 1.0 else 0.0 if g <= 0.0 else g
        b = 1.0 if b >= 1.0 else 0.0 if b <= 0.0 else b

        # Create the instance
        return cls(int(r*BIT_DEPTH), int(g*BIT_DEPTH), int(b*BIT_DEPTH))

    @classmethod
    def hls(cls, h: float, l: float, s: float) -> "Color":
        # TODO: boundary check?
        return cls.rgb(*colorsys.hls_to_rgb(h, l, s))

    @classmethod
    def hsv(cls, h: float, s: float, v: float) -> "Color":
        # TODO: boundary check?
        return cls.rgb(*colorsys.hsv_to_rgb(h, s, v))

    @classmethod
    def yiq(cls, y: float, i: float, q: float) -> "Color":
        # TODO: boundary check?
        return cls.rgb(*colorsys.yiq_to_rgb(y, i, q))

    def __str__(self) -> str:
        return "RGB({}, {}, {})".format(self._r, self._g, self._b)

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b
