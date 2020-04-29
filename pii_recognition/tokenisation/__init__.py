from pii_recognition.registration.registry import Registry
from pii_recognition.tokenisation.detokenisers import (
    Detokeniser,
    SpaceJoinDetokeniser,
    TreebankWordDetokeniser,
)
from pii_recognition.tokenisation.tokenisers import Tokeniser, TreebankWordTokeniser


def tokeniser_init():
    registry = Registry[Tokeniser]()
    registry.add_item(TreebankWordTokeniser)

    return registry


def detokeniser_init():
    registry = Registry[Detokeniser]()
    registry.add_item(SpaceJoinDetokeniser)
    registry.add_item(TreebankWordDetokeniser)


tokeniser_registry: Registry[TreebankWordTokeniser] = tokeniser_init()
