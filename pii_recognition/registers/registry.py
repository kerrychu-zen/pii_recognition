from abc import ABCMeta, abstractmethod
from typing import Generic, Optional, Type, TypeVar

T = TypeVar("T", covariant=True)


class Registry(dict, Generic[T], metaclass=ABCMeta):
    def __init__(self):
        self.add_predefines()

    @abstractmethod
    def add_predefines(self):
        """Use add_item method to put objects to registry."""
        ...

    def add_item(self, item: Type[T], name: Optional[str] = None):
        if name:
            self[name] = item
        else:
            self[getattr(item, "__name__")] = item

    def create_instance(self, name: str, **config) -> T:
        return self[name](**config)
