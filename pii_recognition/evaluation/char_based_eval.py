from typing import Dict, List

from pii_recognition.evaluation.metrics import (compute_label_precision,
                                                compute_label_recall)
from pii_recognition.labels.schema import SpanLabel


def encode_labels(text_length: int, span_labels: List[SpanLabel],
                  label_to_int: Dict) -> List[int]:
    if "default" in label_to_int:
        if label_to_int["default"] != 0:
            raise ValueError("Value of default must be 0!")
        coding = [label_to_int["default"]] * text_length
    else:
        coding = [0] * text_length

    for span in span_labels:
        s = span.start
        e = span.end
        if e > text_length:
            raise ValueError("Span index is out of text range.")
        label_name = span.entity_type
        label_code = label_to_int[label_name]

        coding[s:e] = [label_code] * (e - s)

    return coding


def compute_entity_scores(text: str, true_spans: List[SpanLabel],
                          predicted_spans: List[SpanLabel],
                          label_to_int: Dict) -> Dict[str, List]:
    text_length = len(text)
    true_coding = encode_labels(text_length, true_spans, label_to_int)
    pred_coding = encode_labels(text_length, predicted_spans, label_to_int)

    entity_precisions = []
    for pred_span in predicted_spans:
        span_coding = encode_labels(text_length, [pred_span], label_to_int)
        precision = compute_label_precision(true_coding, span_coding,
                                            pred_span.entity_type)
        entity_precisions.append(precision)

    entity_recalls = []
    for true_span in true_spans:
        span_coding = encode_labels(text_length, [true_span], label_to_int)
        recall = compute_label_recall(span_coding, pred_coding,
                                      true_span.entity_type)
        entity_recalls.append(recall)

    return {
        "predicted_entity_precisions": entity_precisions,
        "true_entities_recalls": entity_recalls
    }
