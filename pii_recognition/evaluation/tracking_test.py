from unittest.mock import patch, call
from .tracking import log_metric_per_entity, mlflow


@patch.object(mlflow, "log_metric")
def test_log_metric_per_entity(mock_log_metric):
    recall = {"PER": 0.8, "LOC": 1.0, "ORG": 0.3}
    log_metric_per_entity(recall, "recall")
    mock_log_metric.assert_has_calls(
        [call("PER_recall", 0.8), call("LOC_recall", 1.0), call("ORG_recall", 0.3)]
    )
