# This is in code review
from pii_recognition.registration.registry import Registry
from pii_recognition.tokenisation.tokenisers import Tokeniser

tokeniser_registry = Registry[Tokeniser]()
