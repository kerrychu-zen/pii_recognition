from __future__ import annotations  # class forward reference

from dataclasses import asdict, dataclass
from typing import NamedTuple

from pii_recognition.tokenisation.token_schema import Token


@dataclass
class SpanLabel:
    entity_type: str
    start: int
    end: int


@dataclass
class TokenLabel(Token):
    entity_type: str

    @classmethod
    def from_instance(cls, instance: Token, entity_type: str) -> TokenLabel:
        return cls(entity_type=entity_type, **asdict(instance))


class EvalLabel(NamedTuple):
    annotated: str
    predicted: str
