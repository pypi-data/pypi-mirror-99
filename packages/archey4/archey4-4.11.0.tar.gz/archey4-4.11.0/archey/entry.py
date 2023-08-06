"""Entry base class"""

from abc import ABC as AbstractBaseClass, abstractmethod

from archey.configuration import Configuration


class Entry(AbstractBaseClass):
    """Module base class"""
    def __new__(cls, *_, **kwargs):
        """Hook object instantiation to handle our particular `disabled` config field"""
        if kwargs.get('options', {}).get('disabled'):
            return None

        return super().__new__(cls)

    @abstractmethod
    def __init__(self, name: str = None, value=None, options: dict = None):
        # Each entry will have always have the following attributes...
        # `name`: key (defaults to the instantiated entry class name);
        # `value`: value of entry as an appropriate object;
        # `options`: configuration options *specific* to an entry instance;
        self.name = name or self.__class__.__name__
        self.value = value
        self.options = options or {}

        # Propagates a reference to default strings specified in `Configuration`.
        self._default_strings = Configuration().get('default_strings')

    def output(self, output):
        """Output the results to output. Can be overridden by subclasses."""
        if self.value:
            # Let's assume we can just use `__str__` on the object in value,
            # and create a single-line output with it.
            output.append(self.name, str(self.value))
        else:
            # If the value is "falsy" leave a generic "Not detected" message for this entry.
            output.append(
                self.name,
                self._default_strings.get('not_detected')
            )
