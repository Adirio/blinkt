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


class Color:
    __slots__ = ('_r', '_g', '_b')

    def __init__(self, r: float=0.0, g: float=0.0, b: float=0.0) -> None:
        pass

    @classmethod
    def rgb(cls, r: int=0, g: int=0, b: int=0) -> "Color":
        return cls()

    @classmethod
    def hls(cls, h: float, l: float, s: float) -> "Color":
        return cls()

    @classmethod
    def hsv(cls, h: float, s: float, v: float) -> "Color":
        return cls()

    @classmethod
    def yiq(cls, y: float, i: float, q: float) -> "Color":
        return cls()

    @property
    def r(self) -> float:
        return 0.0

    @property
    def g(self) -> float:
        return 0.0

    @property
    def b(self) -> float:
        return 0.0
