from typing import Any, Iterable, Optional, Sequence, Type


# TODO: add test
def write_iterable_to_text(iterable: Iterable, file_path: str):
    with open(file_path, "w") as f:
        for elem in iterable:
            f.write(str(elem) + "\n")


class cached_property(property):  # class name follows the convention of property
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        if self.fget is None:
            raise AttributeError("unreadable attribute")

        if obj is None:
            return self

        name = self.fget.__name__
        if name in obj.__dict__:
            return obj.__dict__[name]  # cached already
        else:
            value = self.fget(obj)  # type: ignore
            obj.__dict__[name] = value  # saving back to object
            return value


# TODO: add test
def is_ascending(sequence: Sequence) -> bool:
    return all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))
