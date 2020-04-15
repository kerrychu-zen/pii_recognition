import inspect
from abc import ABCMeta, abstractmethod
from typing import Optional, TypeVar

T = TypeVar("T")


class Registry(dict, metaclass=ABCMeta):
    def __init__(self):
        self.add_predefines()

    @abstractmethod
    def add_predefines(self):
        ...

    def add_item(self, item: T, name: Optional[str]):
        if name:
            self[name] = item
        else:
            name = getattr(item, "__name__")
            self[name] = item
