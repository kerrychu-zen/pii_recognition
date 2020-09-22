import logging
from typing import Dict, List

from pii_recognition.labels.schema import SpanLabel


def encode_labels(
    text_length: int, span_labels: List[SpanLabel], label_to_int: Dict
) -> List[int]:
    if "default" in label_to_int:
        coding = [label_to_int["default"]] * text_length
    else:
        logging.info("Default value 0 is assinged for label encoding.")
        assigned_default = 0
        coding = [assigned_default] * text_length

    for span in span_labels:
        s = span.start
        e = span.end
        if e > text_length:
            raise ValueError(
                f"Span index is out of range: text length is "
                f"{text_length} but got span index {e}."
            )
        label_name = span.entity_type
        label_code = label_to_int[label_name]

        coding[s:e] = [label_code] * (e - s)

    return coding
