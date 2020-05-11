from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple


class Reader(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        ...

    @abstractmethod
    def get_test_data(self, file_path: str, supported_entities: List[str]) -> Data:
        """
        Read test data and split into features and labels, where features are inputs
        to a model and labels are the ground truths.
        """
        ...


@dataclass
class Data:
    # a recogniser takes a string as input so need a setence
    # instead of a list of tokens
    sentences: List[str]
    # labels are token based
    labels: List[List[str]]
    supported_entities: List[str]
