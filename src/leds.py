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
from itertools import cycle
from typing import Sequence, Tuple, Union

from .colors import Color

NUM_LEDS = 8

_instance = None


class Array(tuple):
    class Led:
        __slots__ = ('_i', '_color', '_brightness')

        def __new__(cls, i: int) -> "Led":
            global _instance
            if not _instance:
                _instance = [super(LedArray.Led, cls).__new__(cls) for _ in
                             range(NUM_LEDS)]
            return _instance[i]

        def __init__(self, i: int) -> None:
            self._i = i
            # Color and brightness will be read through their getters so
            # initial values do not matter
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

    _instance = None

    def __new__(cls) -> "Array":
        if not cls._instance:
            cls._instance = super().__new__(
                cls, (Array.Led(i) for i in range(NUM_LEDS)))
        return cls._instance

    def __str__(self) -> str:
        return "[{}]".format(", ".join(map(str, self)))

    @property
    def color(self) -> Tuple[Color, ...]:
        return tuple(led.color for led in self)

    @color.setter
    def color(self, value: Union[Color, Sequence[Color]]) -> None:
        # Handle single items as sequences
        if isinstance(value, Color):
            value = [value]
        # Apply the color in a cycle
        for led, color in zip(self, cycle(value)):
            led.color = color

    @color.deleter
    def color(self) -> None:
        self.color = Color()

    @property
    def brightness(self) -> Tuple[float, ...]:
        return tuple(led.brightness for led in self)

    @brightness.setter
    def brightness(self, value: Union[float, Sequence[float]]) -> None:
        # Handle single items as sequences
        if isinstance(value, float):
            value = [value]
        # Apply the brightness in a cycle
        for led, brightness in zip(self, cycle(value)):
            led.brightness = brightness