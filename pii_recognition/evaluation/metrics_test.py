import numpy as np
import pytest
from numpy.testing import assert_almost_equal

from .metrics import compute_f_beta, compute_label_precision, compute_label_recall


def test_compute_f_beta_for_zero_division():
    actual = compute_f_beta(0.0, 0.0)
    assert np.isnan(actual)


def test_compute_f_beta_for_nan_numerator():
    actual = compute_f_beta(np.nan, 1.0)
    assert np.isnan(actual)


def test_test_compute_f_beta_for_nan_denominator():
    actual = compute_f_beta(1.0, np.nan)
    assert np.isnan(actual)


def test_compute_f_beta():
    actual = compute_f_beta(1.0, 1.0)
    assert actual == 1.0

    actual = compute_f_beta(0.3, 0.5, beta=1.0)
    assert np.isclose(actual, 0.3749999999)

    actual = compute_f_beta(0.3, 0.5, beta=2.0)
    assert np.isclose(actual, 0.44117647058)


def test_compute_label_precision_for_int_labels():
    y_true = [0, 1]
    y_pred = [1, 1]
    actual = compute_label_precision(y_true, y_pred, label_name=1)
    assert actual == 0.5


def test_compute_label_precision_for_str_labels():
    y_true = ["label_0", "label_1"]
    y_pred = ["label_1", "label_1"]
    actual = compute_label_precision(y_true, y_pred, label_name="label_1")
    assert actual == 0.5


def test_compute_label_precision_for_binary():
    y_true = [0, 0, 1]
    y_pred = [0, 1, 1]
    actual = compute_label_precision(y_true, y_pred, label_name=1)
    assert actual == 0.5


def test_compute_label_precision_for_multiclass():
    y_true = [0, 0, 0, 1, 0, 0, 2, 0, 2, "label_0", 0, "label_0", "label_0"]
    y_pred = [0, 0, 0, 1, 1, 1, 2, 2, 2, "label_0", "label_0", "label_0", "label_0"]
    actual = compute_label_precision(y_true, y_pred, label_name=1)
    assert_almost_equal(actual, 0.3333333)
    actual = compute_label_precision(y_true, y_pred, label_name=2)
    assert_almost_equal(actual, 0.6666666)
    actual = compute_label_precision(y_true, y_pred, label_name="label_0")
    assert actual == 0.75


def test_compute_label_precision_for_nonexist_int_labels():
    y_true = [0, 1]
    y_pred = [0, 1]
    actual = compute_label_precision(y_true, y_pred, label_name=2)
    assert actual == 0.0


def test_compute_label_precision_for_nonexist_str_labels():
    y_true = ["label_0", "label_1"]
    y_pred = ["label_0", "label_1"]
    actual = compute_label_precision(y_true, y_pred, label_name="label_2")
    assert actual == 0.0


def test_compute_label_precision_for_nonexist_mixed_labels():
    y_true = [0, 1, "label_0", "label_1"]
    y_pred = [0, 1, "label_0", "label_1"]
    actual = compute_label_precision(y_true, y_pred, label_name=2)
    assert actual == 0.0
    actual = compute_label_precision(y_true, y_pred, label_name="label_2")
    assert actual == 0.0


def test_compute_label_precision_for_str_labels_ask_nonexist_int():
    y_true = ["label_0", "label_1"]
    y_pred = ["label_0", "label_1"]
    actual = compute_label_precision(y_true, y_pred, label_name=1)
    assert actual == 0.0


def test_compute_label_precision_for_int_labels_ask_nonexist_str():
    # This is a very unexpected edge case
    # this happens because y_true will be converted to numpy int
    # but label set gets converted to numpy unicode
    y_true = [0, 1]
    y_pred = [0, 1]
    with pytest.raises(ValueError) as error:
        compute_label_precision(y_true, y_pred, label_name="label_1")
    assert str(error.value) == "y contains previously unseen labels: [0, 1]"


def test_compute_label_recall_for_binary():
    y_true = [0, 1, 1]
    y_pred = [0, 0, 1]
    actual = compute_label_recall(y_true, y_pred, label_name=1)
    assert actual == 0.5


def test_compute_label_recall_for_multiclass():
    y_true = [0, 0, 0, 1, 1, 1, 2, 2, 2, "label_0", "label_0", "label_0", "label_0"]
    y_pred = [0, 0, 0, 1, 0, 0, 2, 0, 2, "label_0", 0, "label_0", "label_0"]
    actual = compute_label_recall(y_true, y_pred, label_name=1)
    assert_almost_equal(actual, 0.3333333)
    actual = compute_label_recall(y_true, y_pred, label_name=2)
    assert_almost_equal(actual, 0.6666666)
    actual = compute_label_recall(y_true, y_pred, label_name="label_0")
    assert actual == 0.75
