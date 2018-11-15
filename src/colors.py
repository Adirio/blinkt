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


class Color:
    __slots__ = ('_r', '_g', '_b')

    def __init__(self, r: float=0.0, g: float=0.0, b: float=0.0) -> None:
        # Check boundaries
        if r < 0.0:
            r = 0.0
        elif r > 1.0:
            r = 1.0
        if g < 0.0:
            g = 0.0
        elif g > 1.0:
            g = 1.0
        if b < 0.0:
            b = 0.0
        elif b > 1.0:
            b = 1.0

        # Store the values
        self._r = r
        self._g = g
        self._b = b

    @classmethod
    def rgb(cls, r: int=0, g: int=0, b: int=0) -> "Color":
        # Check boundaries
        if r < 0:
            r = 0
        elif r > 255:
            r = 255
        if g < 0:
            g = 0
        elif g > 255:
            g = 255
        if b < 0:
            b = 0
        elif b > 255:
            b = 255

        # Create the instance
        return cls(r, g, b)

    @classmethod
    def hls(cls, h: float, l: float, s: float) -> "Color":
        # TODO: boundary check?
        return cls(*colorsys.hls_to_rgb(h, l, s))

    @classmethod
    def hsv(cls, h: float, s: float, v: float) -> "Color":
        # TODO: boundary check?
        return cls(*colorsys.hsv_to_rgb(h, s, v))

    @classmethod
    def yiq(cls, y: float, i: float, q: float) -> "Color":
        # TODO: boundary check?
        return cls(*colorsys.yiq_to_rgb(y, i, q))

    def __str__(self) -> str:
        return "RGB({}, {}, {})".format(
            int(self._r * 255),
            int(self._g * 255),
            int(self._b * 255),
        )

    @property
    def r(self) -> float:
        return self._r

    @property
    def g(self) -> float:
        return self._g

    @property
    def b(self) -> float:
        return self._b
