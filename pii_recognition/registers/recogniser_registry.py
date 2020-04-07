from pii_recognition.recognisers.crf_recogniser import CrfRecogniser
from pii_recognition.recognisers.first_letter_uppercase_recogniser import (
    FirstLetterUppercaseRecogniser,
)
from pii_recognition.recognisers.flair_recogniser import FlairRecogniser
from pii_recognition.recognisers.spacy_recogniser import SpacyRecogniser
from pii_recognition.recognisers.stanza_recogniser import StanzaRecogniser

from .registry import Registry


class RecogniserRegistry(Registry):
    def add_predefines(self):
        self.add_item(CrfRecogniser)
        self.add_item(FirstLetterUppercaseRecogniser)
        self.add_item(FlairRecogniser)
        self.add_item(SpacyRecogniser)
        self.add_item(StanzaRecogniser)
