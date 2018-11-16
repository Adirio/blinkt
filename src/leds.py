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
from .colors import Color

NUM_LEDS = 8

_instance = None


class Led:
    __slots__ = ('_i', '_color', '_brightness')

    def __new__(cls, i: int) -> "Led":
        global _instance
        if not _instance:
            _instance = [super(Led, cls).__new__(cls) for _ in range(NUM_LEDS)]
        return _instance[i]

    def __init__(self, i: int) -> None:
        self._i = i
        # Color and brightness will be read through their getters so initial
        # values do not matter
        self._color = Color()
        self._brightness = 0.0

    def __str__(self) -> str:
        return "<Led {} color={} brightness={}>".format(
            self._i + 1, self._color, self._brightness)

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color) -> None:
        self._color = value

    @color.deleter
    def color(self) -> None:
        self._color = Color()

    @property
    def brightness(self) -> float:
        return self._brightness

    @brightness.setter
    def brightness(self, value: float) -> None:
        self._brightness = value
