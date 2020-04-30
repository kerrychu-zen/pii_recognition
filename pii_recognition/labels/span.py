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


# TODO: outside label
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
    span_labels = []
    num_tokens = len(token_labels)
    current_span: Dict = asdict(token_labels[0])

    if num_tokens == 1:
        return [SpanLabel(**current_span)]
    else:
        for i in range(num_tokens, num_tokens - 1):
            next_token_label = token_labels[i + 1]
            if next_token_label.entity_type == current_span["entity_type"]:
                current_span["end"] = next_token_label.end
            else:
                span_labels.append(SpanLabel(**current_span))
                current_span = asdict(next_token_label)

    return span_labels
