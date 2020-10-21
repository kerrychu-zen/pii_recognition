from typing import Callable, Dict, List, Optional

from boto3.session import Session
from botocore.client import BaseClient
from decouple import config
from pii_recognition.aws.config_session import config_cognito_session
from pii_recognition.labels.schema import Entity

from .entity_recogniser import EntityRecogniser

# read from .env
IDENTITY_POOL_ID = config("IDENTITY_POOL_ID")
AWS_REGION = "us-west-2"


class ModelMapping(dict):
    def __getitem__(self, key: str):
        try:
            return super().__getitem__(key)
        except KeyError:
            key_list = list(super().keys())
            raise ValueError(
                f"Available model names are: {key_list} but got model named {key}"
            )


class ComprehendRecogniser(EntityRecogniser):
    def __init__(
        self,
        supported_entities: List[str],
        supported_languages: List[str],
        model_name: str,
    ):
        sess = config_cognito_session(IDENTITY_POOL_ID, AWS_REGION)
        self.model_name = model_name
        self.comprehend = self._initiate_comprehend(sess)

        super().__init__(
            supported_entities=supported_entities,
            supported_languages=supported_languages,
        )

    @property
    def _model_mapping(self) -> Dict[str, Callable]:
        return ModelMapping(
            ner=self.comprehend.detect_entities, pii=self.comprehend.detect_pii_entities
        )

    def _initiate_comprehend(self, session: Session) -> BaseClient:
        return session.client(service_name="comprehend", region_name=AWS_REGION)

    def analyse(self, text: str, entities: List[str]) -> Optional[List[Entity]]:
        self.validate_entities(entities)

        # TODO: Add multilingual support
        # based on boto3 Comprehend doc Comprehend supports
        # 'en'|'es'|'fr'|'de'|'it'|'pt'|'ar'|'hi'|'ja'|'ko'|'zh'|'zh-TW'
        DEFAULT_LANG = "en"

        model_func = self._model_mapping[self.model_name]
        response = model_func(Text=text, LanguageCode=DEFAULT_LANG)

        # parse response
        predicted_entities = response["Entities"]
        # Remove entities we are not interested
        filtered = filter(lambda ent: ent["Type"] in entities, predicted_entities)
        span_labels = map(
            lambda ent: Entity(ent["Type"], ent["BeginOffset"], ent["EndOffset"]),
            filtered,
        )

        return list(span_labels)
