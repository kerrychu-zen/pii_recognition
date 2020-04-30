from dataclasses import asdict
from typing import List, Tuple, Dict

from pii_recognition.tokenisation.token_schema import Token

from .schema import SpanLabel, TokenLabel


def is_substring(
    segment_A_start_end: Tuple[int, int], segment_B_start_end: Tuple[int, int]
) -> bool:
    """
    Whether segment A is a substring of segment B, where segment is identified by
    indices of the start and end characters.
    """
    if (
        segment_A_start_end[0] >= segment_B_start_end[0]
        and segment_A_start_end[1] <= segment_B_start_end[1]
    ):
        return True
    else:
        return False


def span_labels_to_token_labels(
    span_labels: List[SpanLabel], tokens: List[Token]
) -> List[TokenLabel]:
    """
    A conversion that breaks entity labeled by spans to tokens.

    Args:
        tokens: Text into tokens.
        recognised_entities: Model predicted entities.

    Returns:
        Token based entity labels, e.g., ["O", "O", "LOC", "O"].
    """
    # TODO: add param to control whether to include outside label
    # TODO: span_labels and tokens should be ascending order
    labels = ["O"] * len(tokens)  # default is O, no chunck label

    for i in range(len(tokens)):
        current_token = tokens[i]
        for label in span_labels:
            if is_substring(
                (current_token.start, current_token.end), (label.start, label.end)
            ):
                labels[i] = label.entity_type
                break

    return [TokenLabel.from_instance(tokens[i], labels[i]) for i in range(len(tokens))]


def token_labels_to_span_labels(token_labels: List[TokenLabel]) -> List[SpanLabel]:
    # TODO: token_labels should be ascending order
    span_labels = []
    prior_span: Dict = asdict(token_labels[0])

    for i in range(1, len(token_labels)):
        current_token_label = token_labels[i]
        if current_token_label.entity_type == prior_span["entity_type"]:
            prior_span["end"] = current_token_label.end
        else:
            span_labels.append(SpanLabel(**prior_span))
            prior_span = asdict(current_token_label)

    span_labels.append(SpanLabel(**prior_span))

    return span_labels
