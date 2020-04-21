from typing import Generic, Optional, Type, TypeVar, Dict

T_co = TypeVar("T_co", covariant=True)


class Registry(dict, Generic[T_co]):
    def add_item(self, item: Type[T_co], name: Optional[str] = None):
        if name:
            self[name] = item
        else:
            self[getattr(item, "__name__")] = item

    def create_instance(self, name: str, config: Dict = {}) -> T_co:
        def _create_instance(name: str, **config) -> T_co:
            return self[name](**config)

        return _create_instance(name, **config)
