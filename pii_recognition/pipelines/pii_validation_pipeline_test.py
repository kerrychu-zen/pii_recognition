from mock import patch
from pii_recognition.data_readers.data import Data, DataItem
from pii_recognition.labels.schema import Entity
from pytest import fixture

from .pii_validation_pipeline import identify_pii_entities


@fixture
def data():
    items = [
        DataItem(
            "It's like that since 12/17/1967", true_labels=[Entity("BIRTHDAY", 21, 31)]
        ),
        DataItem(
            "The address of Balefire Global is Valadouro 3, Ubide 48145",
            true_labels=[Entity("ORGANIZATION", 15, 30), Entity("LOCATION", 34, 58)],
        ),
    ]

    return Data(
        items,
        supported_entities={"BIRTHDAY", "ORGANIZATION", "LOCATION"},
        is_io_schema=False,
    )


def analyse_returns():
    return "test"


@patch("pii_recognition.recognisers.comprehend_recogniser.config_cognito_session")
@patch("pii_recognition.recognisers.comprehend_recogniser.ComprehendRecogniser.analyse")
def test_identify_pii_entities_with_comprehend(mock_analyse, mock_session, data):
    mock_analyse.return_value = [Entity("test", 0, 4)]

    recogniser_name = "ComprehendRecogniser"
    recogniser_params = {
        "supported_entities": [
            "COMMERCIAL_ITEM",
            "DATE",
            "EVENT",
            "LOCATION",
            "ORGANIZATION",
            "OTHER",
            "PERSON",
            "QUANTITY",
            "TITLE",
        ],
        "supported_languages": ["en"],
    }

    data = identify_pii_entities(data, recogniser_name, recogniser_params)
    assert [item.pred_labels for item in data.items] == [
        [Entity("test", 0, 4)],
        [Entity("test", 0, 4)],
    ]
