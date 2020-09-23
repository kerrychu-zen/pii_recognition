from typing import List

import numpy as np
from sklearn.metrics import precision_score, recall_score


def compute_f_beta(precision: float, recall: float, beta: float = 1.0) -> float:
    if np.isnan(precision) or np.isnan(recall) or (precision == 0 and recall == 0):
        return np.nan

    return ((1 + beta ** 2) * precision * recall) / (((beta ** 2) * precision) + recall)


def compute_label_precision(
    y_true: List[str], y_pred: List[str], label_name: str,
) -> float:
    """Compute recall for a designated label.

    This can calculate precision of a particular label for both binary and multi-class
    settings. The called upon sklearn function is not stable on string and integer mixed
    labels, may encouter ValueError. So input arguments are required to be in str.
    """
    return precision_score(y_true, y_pred, average=None, labels=[label_name])[0]


def compute_label_recall(
    y_true: List[str], y_pred: List[str], label_name: str,
) -> float:
    """Compute recall for a designated label.

    This can calculate recall of a particular label for both binary and multi-class
    settings. The called upon sklearn function is not stable on string and integer mixed
    labels, may encouter ValueError. So input arguments are required to be in str.
    """
    return recall_score(y_true, y_pred, average=None, labels=[label_name])[0]
