from typing import List

import boto3
from boto3 import Session

from pii_recognition.labels.schema import SpanLabel

from .entity_recogniser import EntityRecogniser


class ComprehendRecogniser(EntityRecogniser):
    def __init__(self, supported_entities: List[str],
                 supported_languages: List[str]):
        self.comprehend = self._init_comprehend()

        super().__init__(supported_entities=supported_entities,
                         supported_languages=supported_languages)

    def _init_comprehend(self) -> Session:
        # TODO: Authenticate service
        return boto3.client(service_name="comprehend", region_name="us-west-2")

    def analyse(self, text: str, entities: List[str]) -> List[SpanLabel]:
        # TODO: Add multilingual support but now only modeling on English.
        DEFAULT_LANG = 'en'
        predicted_entities = self.comprehend.detect_entities(
            Text=text, LanguageCode=DEFAULT_LANG)
        # TODO: Convert entities to type of span label
        return predicted_entities
