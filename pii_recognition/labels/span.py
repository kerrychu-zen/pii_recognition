from typing import List, Tuple

from pii_recognition.tokenisation.token_schema import Token

from .schema import SpanLabel, TokenLabel


def is_substring(
    segment_A_start_end: Tuple[int, int], segment_B_start_end: Tuple[int, int]
) -> bool:
    """
    Whether segment A is a substring of segment B, where segment is identified by
    position of the start and end characters.
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
    segment_start = token_labels[0].start
    segment_end = token_labels[0].end

    if len(token_labels) == 1:
        return [SpanLabel(token_labels[0].entity_type, segment_start, segment_end)]

    # process all except the last one
    for i in range(1, len(token_labels)):
        if token_labels[i].entity_type == token_labels[i - 1].entity_type:
            segment_end = token_labels[i].end
        else:
            span_labels.append(
                SpanLabel(token_labels[i - 1].entity_type, segment_start, segment_end)
            )
            segment_start = token_labels[i].start
            segment_end = token_labels[i].end

    # write out the last one
    segment_end = token_labels[-1].end
    span_labels.append(
        SpanLabel(token_labels[-1].entity_type, segment_start, segment_end)
    )
    return span_labels
