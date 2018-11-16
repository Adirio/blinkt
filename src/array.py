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
from .leds import Led, NUM_LEDS


class LedArray(tuple):
    _instance = None

    def __new__(cls) -> "LedArray":
        if not cls._instance:
            cls._instance = super().__new__(
                cls, (Led(i) for i in range(NUM_LEDS)))
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
