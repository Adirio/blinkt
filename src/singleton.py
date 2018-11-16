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


class Singleton(type):
    """
    Metaclass that turns the class into a singleton

    It uses a class variable to store the single instance which is created at
    class creation by calling its constructor with no arguments. This means
    that this method does not support classes that require initialization
    parameters. However, singletons should not need initialization parameters
    as they only have one instance.

    Usage:
        class SingletonExample(metaclass=Singleton):
            def __init__(self):
                pass
    """
    _attribute = '__singleton'

    def __new__(mcs, name, bases, classdict):
        # Name mangling
        singleton_attribute = mcs.mangle_attribute(name, mcs._attribute)

        # Panic if it is already used
        if singleton_attribute in classdict:
            raise AttributeError(
                "Singleton pattern uses {}.{} but it was already defined in "
                "the class".format(name, mcs._attribute)
            )

        # Create the class
        cls = super().__new__(mcs, name, bases, classdict)

        # Create the single instance and store it
        setattr(cls, singleton_attribute, cls())

        # Replace the constructor method
        cls.__new__ = lambda kls: getattr(kls, singleton_attribute)

        return cls

    @staticmethod
    def mangle_attribute(name, attribute):
        """
        Mangle private attributes:
            cls.attribute     => cls.attribute
            cls._attribute    => cls._attribute
            cls.__attribute   => cls._name__attribute  <-----
            cls.__attribute__ => cls.__attribute__
        """
        if attribute.startswith('__') and not attribute.endswith('__'):
            attribute = '_' + name + attribute
        return attribute
