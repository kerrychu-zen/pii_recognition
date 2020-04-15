from abc import ABCMeta, abstractmethod
from typing import Generic, Optional, Type, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Registry(dict, Generic[T_co], metaclass=ABCMeta):
    def __init__(self):
        self.add_predefines()

    @abstractmethod
    def add_predefines(self):
        """Use add_item method to put objects to registry."""
        ...

    def add_item(self, item: Type[T_co], name: Optional[str] = None):
        if name:
            self[name] = item
        else:
            self[getattr(item, "__name__")] = item

    def create_instance(self, name: str, **config) -> T_co:
        return self[name](**config)
