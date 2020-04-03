import re
from typing import Match, Optional, Type


class Path:
    _pattern_str: Optional[str] = None
    valid: bool = False

    def __init__(self, path: str):
        self.path = path
        matches = self.get_pattern()
        if matches is None:
            self.valid = True
        else:
            self._pattern_to_attrs(matches)

    def get_pattern(self) -> Optional[Match]:
        if not self._pattern_str:
            raise AttributeError("No pattern has been defined.")

        return re.match(self._pattern_str, self.path)

    def _pattern_to_attrs(self, pattern: Match):
        for key, value in pattern.groupdict().items():
            setattr(self, key, value)


def create_path_subclass(cls_name: str, pattern: str) -> Type[Path]:
    return type(cls_name, (Path,), {"_pattern_str": pattern})
