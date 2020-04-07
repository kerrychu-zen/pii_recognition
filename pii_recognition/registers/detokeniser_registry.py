from pii_recognition.tokenisation.detokenisers import (
    space_join_detokensier,
    treebank_detokeniser,
)

from .registry import Registry


class DetokeniserRegistry(Registry):
    def add_predefines(self):
        self.add_item(space_join_detokensier)
        self.add_item(treebank_detokeniser)
