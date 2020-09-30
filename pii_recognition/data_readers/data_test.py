from typing import List

import pytest

from .data import Data
from pii_recognition.labels.schema import Entity


def test_Data_token_labels():
    texts = ["A tribute to Joshua Lewis", "It's like that since 12/17/1967"]
    labels = [
        ["O", "O", "O", "B-PERSON", "I-PERSON"],
        ["O", "O", "O", "O", "O", "U-BIRTHDAY"],
    ]

    data = Data(
        texts=texts,
        labels=labels,
        supported_entities={"I-PERSON", "U-BIRTHDAY"},
        is_io_schema=True,
    )
    assert data.texts == texts
    assert data.labels == labels
    assert data.supported_entities == {"I-PERSON", "U-BIRTHDAY"}
    assert data.is_io_schema


def test_Data_span_labels():
    texts = ["A tribute to Joshua Lewis", "It's like that since 12/17/1967"]
    labels = [
        [Entity(entity_type="PERSON", start=13, end=25)],
        [Entity(entity_type="BIRTHDAY", start=21, end=31)],
    ]

    data = Data(
        texts=texts,
        labels=labels,
        supported_entities={"PERSON", "BIRTHDAY"},
        is_io_schema=False,
    )
    assert data.texts == texts
    assert data.labels == labels
    assert data.supported_entities == {"PERSON", "BIRTHDAY"}
    assert data.is_io_schema is False


def test_Data_for_texts_labels_length_mismatch():
    texts = ["A tribute to Joshua Lewis", "It's like that since 12/17/1967"]
    labels: List = []

    with pytest.raises(AssertionError) as err:
        Data(
            texts=texts,
            labels=labels,
            supported_entities={"PERSON"},
            is_io_schema=False,
        )
    assert str(err.value) == (
        "Texts length does not match with labels length: "
        "texts length is 2 and labels length is 0"
    )
