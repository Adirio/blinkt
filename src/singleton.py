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
from typing import Any, Dict, Tuple


def mangle(class_name: str, attribute: str) -> str:
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
    Metaclass that turns the class into a singleton lazily initialized

    It uses a class variable to store the single instance which is created at
    class creation by calling its constructor with no arguments. This means
    that this method does not support classes that require initialization
    parameters. However, singletons should not need initialization parameters
    as they only have one instance.

    The private class attributes __instance and __new are used internally.
    If they want to be used by the class, another attribute name should be
    provided through the `instance` or `constructor` keyword argument of the
    class respectively.

    Usage:
        class SingleExample(metaclass=Singleton):
            def __init__(self):
                pass

        class SingleExample2(metaclass=Singleton, constructor='__qwerty'):
            __new = "my class variable"
            def __init__(self):
                pass

        class SingleExample3(metaclass=Singleton, instance='__asdfg'):
            __instance = "my class variable"
            def __init__(self):
                pass

        class SingleExample4(metaclass=Singleton, constructor='__qwerty',
                             instance='__asdfg'):
            __new = "my class variable"
            __instance = "my class variable"
            def __init__(self):
                pass
    """
    def __new__(
            mcs,
            name: str,
            bases: Tuple,
            namespace: Dict[str, Any],
            constructor: str='__new',
            **kwargs,
    ) -> type:
        # Name mangling
        mangled_constructor = mangle(name, constructor)

        # Panic if constructor attribute is already used
        if mangled_constructor in namespace:
            raise AttributeError(
                "Singleton pattern uses {}.{} but it was already defined in "
                "the class".format(name, constructor))

        # Store the previous constructor if exists
        if '__new__' in namespace:
            namespace[mangled_constructor] = namespace['__new__']
            del namespace['__new__']

        return super().__new__(mcs, name, bases, namespace)

    def __init__(
            cls,
            name: str,
            bases: Tuple,
            namespace: Dict[str, Any],
            constructor: str='__new',
            instance: str='__instance',
    ) -> None:
        # Name mangling
        mangled_constructor = mangle(name, constructor)
        mangled_instance = mangle(name, instance)

        # Panic if instance attribute is already used
        if mangled_instance in namespace:
            raise AttributeError(
                "Singleton pattern uses {}.{} but it was already defined in "
                "the class".format(name, instance))

        # Extract the constructor method as we are going to replace it
        new = namespace.pop(mangled_constructor, cls.__new__)

        # Method to return the pre-created singleton instance
        def get_instance(kls):
            return getattr(kls, mangled_instance)

        # Wrapped constructor method
        def wrapped_new(kls):
            # Create the single instance and store it
            setattr(kls, mangled_instance, new(kls))
            # Replace the constructor method and execute it
            kls.__new__ = get_instance
            return kls.__new__(kls)

        # Follow the init chain
        super().__init__(name, bases, namespace)

        # Assign the first time constructor to the class
        cls.__new__ = wrapped_new
