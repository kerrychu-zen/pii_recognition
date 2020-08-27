from typing import List

import boto3
from boto3.session import Session
from botocore.client import BaseClient
from decouple import config

from pii_recognition.labels.schema import SpanLabel

from .entity_recogniser import EntityRecogniser

IDENTITY_POOL_ID = config("IDENTITY_POOL_ID")
AWS_REGION = "us-west-2"


class ComprehendRecogniser(EntityRecogniser):
    def __init__(self, supported_entities: List[str],
                 supported_languages: List[str]):
        sess = self._create_boto3_session(IDENTITY_POOL_ID)
        self.comprehend = self._initiate_comprehend(sess)

        super().__init__(supported_entities=supported_entities,
                         supported_languages=supported_languages)

    def _create_boto3_session(self, identity_pool_id: str) -> Session:
        client = boto3.client(service_name='cognito-identity',
                              region_name="us-west-2")

        response = client.get_id(IdentityPoolId=IDENTITY_POOL_ID)
        identity_id = response["IdentityId"]

        response = client.get_credentials_for_identity(IdentityId=identity_id)
        secretKey = response['Credentials']['SecretKey']
        accessKey = response['Credentials']['AccessKeyId']
        sessionToken = response['Credentials']['SessionToken']

        return Session(aws_access_key_id=accessKey,
                       aws_secret_access_key=secretKey,
                       aws_session_token=sessionToken,
                       region_name=AWS_REGION)

    def _initiate_comprehend(self, session: Session) -> BaseClient:
        return session.client(service_name="comprehend",
                              region_name=AWS_REGION)

    def analyse(self, text: str, entities: List[str]) -> List[SpanLabel]:
        # TODO: Add multilingual support but now only modeling on English.
        DEFAULT_LANG = 'en'

        response = self.comprehend.detect_entities(Text=text,
                                                   LanguageCode=DEFAULT_LANG)
        predicted_entities = response["Entities"]

        # TODO: Consider add score to dataclass
        span_labels = list(
            map(
                lambda entity: SpanLabel(entity["Type"], entity[
                    "BeginOffset"], entity["EndOffset"]), predicted_entities))
        return span_labels
