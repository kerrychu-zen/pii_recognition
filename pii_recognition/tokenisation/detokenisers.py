from abc import ABCMeta, abstractmethod
from typing import Callable, List

import nltk

from pii_recognition.utils import cached_property


class Detokeniser(metaclass=ABCMeta):
    @abstractmethod
    def detokenise(self, tokens: List[str]) -> str:
        ...


class SpaceJoinDetokeniser(Detokeniser):
    def detokenise(self, tokens: List[str]) -> str:
        return " ".join(tokens)


class TreebankDetokeniser(Detokeniser):
    @cached_property
    def _engine(self):
        return nltk.tokenize.treebank.TreebankWordDetokenizer()

    def detokenise(self, tokens: List[str]) -> str:
        return self._engine.detokenize(tokens)
