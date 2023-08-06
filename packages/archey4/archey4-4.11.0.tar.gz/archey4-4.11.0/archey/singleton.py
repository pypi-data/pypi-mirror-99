"""Simple singleton meta-class definition"""


from abc import ABCMeta as AbstractBaseMetaClass
from typing import Dict, Type


class Singleton(AbstractBaseMetaClass):
    """
    Taken from : <https://stackoverflow.com/q/6760685/10599709>
    This meta-class allows us to declare `Configuration` as a singleton.
    This way, we are able to import `Configuration` in multiple modules, ...
    ... whereas it is effectively loaded only once.
    You cannot instantiate this meta-class directly.
    """
    _instances: Dict[Type['Singleton'], object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
