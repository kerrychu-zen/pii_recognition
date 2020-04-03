import re
from typing import Match, Optional, Type
from abc import ABCMeta, abstractmethod


class Path(metaclass=ABCMeta):
    valid: bool = False

    def __init__(self, path: str):
        self.path = path
        matches = self.get_pattern()
        if matches is None:
            self.valid = True
        else:
            self._pattern_to_attrs(matches)

    @property
    @abstractmethod
    def pattern_str(self) -> str:
        ...

    def get_pattern(self) -> Optional[Match]:
        return re.match(self.pattern_str, self.path)

    def _pattern_to_attrs(self, pattern: Match):
        for key, value in pattern.groupdict().items():
            setattr(self, key, value)


def create_path_subclass(cls_name: str, pattern: str) -> Type[Path]:
    return type(cls_name, (Path,), {"_pattern_str": pattern})
