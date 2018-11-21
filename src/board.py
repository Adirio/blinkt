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
from threading import Lock
from time import sleep
from types import TracebackType
from typing import Optional, Type

from .leds import Array
from .singleton import Singleton

# import RPi.GPIO as GPIO

# CHANNEL_MODE = GPIO.BOARD
DATA_CHANNEL = 16
CLOCK_CHANNEL = 18
CLOCK_PERIOD = 0.000001


class Error(Exception):
    """Base module exception"""


class DisplayError(Error):
    """Display-related errors"""


class Board(metaclass=Singleton):
    """
    Virtual representation of a Blinkt board

    It has two properties: `leds` (read-only) and `clear`.

    It acts as a context manager, allowing to call the `display` method to copy
    the virtual `leds` state to the physical board.

    This class is completely thread-safe, even opening contexts from different
    threads is allowed.
    """

    __slots__ = ('_array', '_clear', '_lock', '_counter', '_half_period')

    def __init__(self) -> None:
        self._array = Array()
        self._clear = False
        self._lock = Lock()
        self._counter = 0
        self._half_period = CLOCK_PERIOD / 2

    def __str__(self) -> str:
        return "<Blinkt {}>".format(self._array)

    def __enter__(self) -> "Board":
        """Setup the board"""
        with self._lock:
            # Setup the GPIO if it is unset
            if self._counter == 1:
                # GPIO.setmode(CHANNEL_MODE)
                # GPIO.setwarnings(False)
                # GPIO.setup(DATA_CHANNEL, GPIO.OUT)
                # GPIO.setup(CLOCK_CHANNEL, GPIO.OUT)
                pass

            # Increment the counter
            self._counter += 1

        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[Exception],
            exc_tb: Optional[TracebackType],
    ) -> bool:
        """Cleanup the board"""
        with self._lock:
            # Decrease the counter
            self._counter -= 1

            if self._counter == 0:
                # Shut off the leds if specified
                if self._clear:
                    del self._array.color
                    self._display()

                # Cleanup the GPIO
                # GPIO.cleanup()

        # Raise exceptions if any
        return False

    @property
    def leds(self) -> Array:
        """
        Immutable sequence of led objects

        Each led object has color (type Color) and brightness (type float,
        range 0..1) properties that can be set or read. Additionally they are
        also context managers, which will grant led ownership to the current
        thread meaning that its state can not be modified from a different one
        until it is released.

        The sequence object also offers color and brightness properties that
        return a tuple of the individuals properties. Setting them will have a
        cyclic behaviour, repeating the provided sequence as needed to cover
        all the led objects. Is also acts as a context manager, grabbing
        ownership of all the led objects.
        """
        return self._array

    @property
    def clear(self) -> bool:
        """Whether the leds will be shut down when the device is released"""
        return self._clear

    @clear.setter
    def clear(self, value: bool) -> None:
        self._clear = value

    @clear.deleter
    def clear(self) -> None:
        self._clear = False

    def _clock(self) -> None:
        # GPIO.output(CLOCK_CHANNEL, True)
        sleep(self._half_period)
        # GPIO.output(CLOCK_CHANNEL, False)
        sleep(self._half_period)

    def _send_bit(self, value: bool) -> None:
        print(str(int(value)), end='')  # GPIO.output(DATA_CHANNEL, value)
        self._clock()

    def _send_bits(self, value: bool, n: int) -> None:
        print(str(int(value))*n, end='')  # GPIO.output(DATA_CHANNEL, value)
        for _ in range(n):
            self._clock()

    def _display(self) -> None:
        print("Sending: ", end='')
        # Start frame
        self._send_bits(False, 32)
        print()
        # Led frames
        for led in self._array:
            color, brightness = led.all
            # First byte: 1110 0000 & brightness (000x xxxx) = 111x xxxx
            self._send_bits(True, 3)
            for bit in ((brightness >> i) & 1 for i in range(4, -1, -1)):
                self._send_bit(bit)
            print(' ', end='')
            # Second byte: blue
            for bit in ((color.b >> i) & 1 for i in range(7, -1, -1)):
                self._send_bit(bit)
            print(' ', end='')
            # Second byte: green
            for bit in ((color.g >> i) & 1 for i in range(7, -1, -1)):
                self._send_bit(bit)
            print(' ', end='')
            # Second byte: red
            for bit in ((color.r >> i) & 1 for i in range(7, -1, -1)):
                self._send_bit(bit)
            print()
        # End frame
        self._send_bits(True, (len(self._array) + 1) // 2)
        print()

    def display(self) -> None:
        with self._lock:
            if self._counter > 0:
                self._display()
