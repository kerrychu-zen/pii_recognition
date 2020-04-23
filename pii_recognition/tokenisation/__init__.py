from pii_recognition.registration.registry import Registry
from pii_recognition.tokenisation.tokenisers import Tokeniser, TreebankWordTokeniser


def init():
    registry = Registry[Tokeniser]()
    registry.add_item(TreebankWordTokeniser)

    return registry


tokeniser_registry: Registry[TreebankWordTokeniser] = init()
