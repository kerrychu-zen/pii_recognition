from abc import ABCMeta, abstractmethod
from typing import Callable, List

from nltk.tokenize.treebank import TreebankWordDetokenizer


class Detokeniser(metaclass=ABCMeta):
    @abstractmethod
    def detokenise(self, tokens: List[str]) -> str:
        ...


class SpaceJoinDetokeniser(Detokeniser):
    def detokenise(self, tokens: List[str]) -> str:
        return " ".join(tokens)


def treebank_detokeniser(tokens: List[str]) -> str:
    return TreebankWordDetokenizer().detokenize(tokens)
