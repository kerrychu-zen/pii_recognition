from dataclasses import dataclass


@dataclass
class Token:
    start: int
    end: int
