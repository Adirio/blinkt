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
from threading import RLock, Lock
from types import TracebackType
from typing import Optional, Sequence, Tuple, Type, Union

from .colors import Color
from .singleton import Singleton

NUM_LEDS = 8


class _Tuple(tuple):
    """Adapter class that removes keyword-arguments from __init_subclass__"""
    def __init_subclass__(cls, **kwargs):
        """Remove keyword-arguments as tuple do not accept them"""
        return super().__init_subclass__()


class Array(_Tuple, metaclass=Singleton):
    class Led:
        __slots__ = ('_color', '_brightness', '_lock', '_ownership')

        def __init__(self) -> None:
            self._color = Color()
            self._brightness = 0.0
            self._lock = Lock()
            self._ownership = RLock()

        def __str__(self) -> str:
            with self._lock:
                return "<Led color={} brightness={}>".format(
                    self._color, self._brightness)

        def __enter__(self) -> "Array.Led":
            # Initialization
            self._ownership.acquire()

            # Return itself
            return self

        def __exit__(
                self,
                exc_type: Optional[Type[BaseException]],
                exc_val: Optional[Exception],
                exc_tb: Optional[TracebackType],
        ) -> bool:
            # Finalization
            self._ownership.release()

            # Short-circuit for non-exceptional execution
            if all(map(lambda x: x is None, (exc_type, exc_val, exc_tb))):
                return True

            # Handle exceptions: return True to omit and False to raise
            return False

        @property
        def color(self) -> Color:
            with self._lock:
                return self._color

        @color.setter
        def color(self, value: Color) -> None:
            with self._ownership, self._lock:
                self._color = value

        @color.deleter
        def color(self) -> None:
            with self._ownership, self._lock:
                self._color = Color()

        @property
        def brightness(self) -> float:
            with self._lock:
                return self._brightness

        @brightness.setter
        def brightness(self, value: float) -> None:
            with self._ownership, self._lock:
                self._brightness = value

    def __new__(cls) -> "Array":
        array = super().__new__(cls, (cls.Led() for _ in range(NUM_LEDS)))
        array._lock = Lock()
        array._ownership = RLock()
        return array

    def __str__(self) -> str:
        with self._lock:
            return "[{}]".format(", ".join(map(str, self)))

    def __enter__(self) -> "Array":
        # Initialization
        self._ownership.acquire()
        for led in self:
            led.__enter__()

        # Return itself
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[Exception],
            exc_tb: Optional[TracebackType],
    ) -> bool:
        # Finalization
        results = []
        for led in self:
            results.append(led.__exit__(exc_type, exc_val, exc_tb))
        self._ownership.release()

        # Handle exceptions: return True to omit and False to raise
        return all(results)

    @property
    def color(self) -> Tuple[Color, ...]:
        with self._lock:
            return tuple(led.color for led in self)

    @color.setter
    def color(self, value: Union[Color, Sequence[Color]]) -> None:
        # Handle single items as sequences
        if isinstance(value, Color):
            value = [value]
        # Apply the color in a cycle
        with self._ownership, self._lock:
            for led, color in zip(self, cycle(value)):
                led.color = color

    @color.deleter
    def color(self) -> None:
        with self._ownership, self._lock:
            for led in self:
                del led.color

    @property
    def brightness(self) -> Tuple[float, ...]:
        with self._lock:
            return tuple(led.brightness for led in self)

    @brightness.setter
    def brightness(self, value: Union[float, Sequence[float]]) -> None:
        # Handle single items as sequences
        if isinstance(value, float):
            value = [value]
        # Apply the brightness in a cycle
        with self._ownership, self._lock:
            for led, brightness in zip(self, cycle(value)):
                led.brightness = brightness
