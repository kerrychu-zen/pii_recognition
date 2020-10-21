from unittest.mock import MagicMock, patch

from moto import mock_cognitoidentity
import pytest
from pii_recognition.labels.schema import Entity
from pii_recognition.recognisers.comprehend_recogniser import ComprehendRecogniser


@pytest.fixture
def fake_response():
    return {
        "Entities": [
            {
                "Score": 0.9941786527633667,
                "Type": "OTHER",
                "Text": "5467800309398046",
                "BeginOffset": 83,
                "EndOffset": 99,
            },
            {
                "Score": 0.7360825538635254,
                "Type": "LOCATION",
                "Text": "23 Settlement Road, WINNINDOO 3858",
                "BeginOffset": 137,
                "EndOffset": 171,
            },
        ],
        "ResponseMetadata": {
            "RequestId": "2f4c22b8-9f25-4b01-8a60-49280daf1979",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "2f4c22b8-9f25-4b01-8a60-49280daf1979",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "241",
                "date": "Mon, 31 Aug 2020 05:55:12 GMT",
            },
            "RetryAttempts": 0,
        },
    }


# @patch("pii_recognition.recognisers.comprehend_recogniser.config_cognito_session")
# def test_comprehend_recogniser_analyse_for_ner_model(mock_session, fake_response):
#     mocked_comprehend = MagicMock()
#     mocked_comprehend.detect_entities.return_value = fake_response

#     fake_text = (
#         "Could you please email me the statement for laste month , "
#         "my credit card number is 5467800309398046? Also, how do I "
#         "change my address to 23 Settlement Road, WINNINDOO 3858 for "
#         "post mail?"
#     )

#     recogniser = ComprehendRecogniser(
#         supported_entities=[
#             "COMMERCIAL_ITEM",
#             "DATE",
#             "EVENT",
#             "LOCATION",
#             "ORGANIZATION",
#             "OTHER",
#             "PERSON",
#             "QUANTITY",
#             "TITLE",
#         ],
#         supported_languages=["en"],
#         model_name="ner",
#     )
#     recogniser.comprehend = mocked_comprehend

#     spans = recogniser.analyse(fake_text, recogniser.supported_entities)
#     assert spans == [Entity("OTHER", 83, 99), Entity("LOCATION", 137, 171)]

#     spans = recogniser.analyse(fake_text, ["OTHER"])
#     assert spans == [
#         Entity("OTHER", 83, 99),
#     ]

#     spans = recogniser.analyse(fake_text, ["LOCATION"])
#     assert spans == [Entity("LOCATION", 137, 171)]

#     with pytest.raises(AssertionError) as err:
#         recogniser.analyse(
#             fake_text, entities=["THOSE", "ENTITIES", "NOT", "SUPPORTED"]
#         )
#     assert str(err.value) == (
#         "Only support ['COMMERCIAL_ITEM', 'DATE', 'EVENT', 'LOCATION', 'ORGANIZATION', "
#         "'OTHER', 'PERSON', 'QUANTITY', 'TITLE'], but got ['THOSE', 'ENTITIES', 'NOT', "
#         "'SUPPORTED']"
#     )


@mock_cognitoidentity
def test_comprehend_recogniser_for_initialisation_ner_model():
    actual = ComprehendRecogniser(
        supported_entities=["test"], supported_languages=["test"], model_name="ner"
    )
    assert actual.model_name == "ner"
    assert actual.supported_entities == ["test"]
    assert actual.supported_languages == ["test"]


@mock_cognitoidentity
def test_comprehend_recogniser_for_initialisation_pii_model():
    actual = ComprehendRecogniser(
        supported_entities=["test"], supported_languages=["test"], model_name="pii"
    )
    assert actual.model_name == "pii"
    assert actual.supported_entities == ["test"]
    assert actual.supported_languages == ["test"]


@mock_cognitoidentity
def test_comprehend_recogniser_for_initialisation_invalid_model():
    with pytest.raises(ValueError) as err:
        ComprehendRecogniser(
            supported_entities=["test"],
            supported_languages=["test"],
            model_name="invalid",
        )
    assert str(err.value) == (
        "Available model names are: {'pii', 'ner'} but got model named invalid"
    )
