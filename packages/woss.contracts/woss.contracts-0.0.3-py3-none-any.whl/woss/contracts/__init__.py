"""

"""

import inspect


__version__ = '0.0.3'


class Contract(type):
    """

    """

    def __subclasscheck__(self, subclass) -> bool:
        return all(
            self.has(subclass, *func)
            for func in inspect.getmembers(self, inspect.isfunction)
        )

    def __instancecheck__(self, instance) -> bool:
        return issubclass(instance.__class__, self)

    def has(self, subclass, name, function) -> bool:
        if not hasattr(subclass, name):
            return False
        return self.validate(function, getattr(subclass, name))

    @property
    def validators(self):
        yield from (
            value
            for name, value in inspect.getmembers(inspect, inspect.isfunction)
            if name.startswith('is')
        )

    def validate(self, expected, received) -> bool:
        if not all(
            validator(expected) == validator(received)
            for validator in self.validators
        ):
            return False

        return inspect.signature(expected) == inspect.signature(received)
