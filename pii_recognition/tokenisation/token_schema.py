from dataclasses import dataclass


@dataclass
class Token:
    # text is not included on purpose, otherwise it would make
    # conversion between SpanLabel and TokenLabel difficult
    text: str
    start: int
    end: int
