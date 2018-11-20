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


def mangle(class_name, attribute):
    """
    Mangle private attributes:
        cls.attribute     => cls.attribute
        cls._attribute    => cls._attribute
        cls.__attribute   => cls._name__attribute  <-----
        cls.__attribute__ => cls.__attribute__
    """
    if attribute.startswith('__') and not attribute.endswith('__'):
        attribute = '_' + class_name + attribute
    return attribute


class Singleton(type):
    """
    Metaclass that turns the class into a singleton

    It uses a class variable to store the single instance which is created at
    class creation by calling its constructor with no arguments. This means
    that this method does not support classes that require initialization
    parameters. However, singletons should not need initialization parameters
    as they only have one instance.

    The private class attribute __instance is used internally. If this wants to
    be used by the class, another attribute name should be provided through the
    instance class keyword argument.

    Usage:
        class SingleExample(metaclass=Singleton):
            def __init__(self):
                pass

        class SingleExample2(metaclass=Singleton, instance='__qwerty'):
            __instance = "my class variable"
            def __init__(self):
                pass
    """
    def __init__(cls, name, bases, attrs, instance='__instance'):
        # Name mangling
        mangled_instance = mangle(name, instance)

        # Panic if it is already used
        if mangled_instance in attrs:
            raise AttributeError(
                "Singleton pattern uses {}.{} but it was already defined in "
                "the class".format(name, instance)
            )

        # Create the single instance and store it
        setattr(cls, mangled_instance, cls())

        # Replace the constructor method
        cls.__new__ = lambda kls: getattr(kls, mangled_instance)

        super().__init__(name, bases, attrs)
