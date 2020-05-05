import os
from tempfile import TemporaryDirectory
from unittest.mock import call, patch

import mlflow

from .tracking import log_metric_per_entity, mlflow, start_tracker


def test_start_tracker_fresh_start():
    with TemporaryDirectory() as tempdir:
        start_tracker("TEST-EXP", "TEST-RUN", tempdir)
        assert mlflow.active_run().info.run_id is not None
        assert mlflow.active_run().info.experiment_id == "0"
        # terminate an active run
        mlflow.end_run()


def test_start_tracker_reload_experiment():
    with TemporaryDirectory() as tempdir:
        start_tracker("TEST-EXP", "TEST-RUN", tempdir)
        # terminate an active run
        mlflow.end_run()

        start_tracker("TEST-EXP", "TEST-RUN", tempdir)
        assert mlflow.active_run().info.run_id is not None
        assert mlflow.active_run().info.experiment_id == "0"
        # terminate an active run
        mlflow.end_run()


@patch.object(mlflow, "log_metric")
def test_log_metric_per_entity(mock_log_metric):
    recall = {"PER": 0.8, "LOC": 1.0, "ORG": 0.3}
    log_metric_per_entity(recall, "recall")
    mock_log_metric.assert_has_calls(
        [call("PER_recall", 0.8), call("LOC_recall", 1.0), call("ORG_recall", 0.3)]
    )
