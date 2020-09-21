from typing import Any, List, Union

import numpy as np
from sklearn.metrics import precision_score, recall_score


def compute_f_beta(precision: float,
                   recall: float,
                   beta: float = 1.0) -> float:
    if np.isnan(precision) or np.isnan(recall) or (precision == 0
                                                   and recall == 0):
        return np.nan

    return ((1 + beta**2) * precision * recall) / ((
        (beta**2) * precision) + recall)


def compute_label_precision(y_true: List, y_pred: List,
                            label_name: Union[int, str]) -> float:
    """Compute recall for a designated label.

    This can calculate precision for both binary and multi-class labels, however, users
    must be aware in sklearn 0 is reserved, that is, labels not present in the data will
    result in 0 components.
    """
    return precision_score(y_true, y_pred, average=None,
                           labels=[label_name])[0]


def compute_label_recall(y_true: List, y_pred: List,
                         label_name: Union[int, str]) -> float:
    """Compute recall for a designated label.

    This can calculate recall for both binary and multi-class labels, however, users
    must be aware in sklearn 0 is reserved, that is, labels not present in the data
    will result in 0 components.
    """
    return recall_score(y_true, y_pred, average=None, labels=[label_name])[0]
