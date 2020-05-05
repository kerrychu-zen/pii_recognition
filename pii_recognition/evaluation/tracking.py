"""
Tracker module implementing Mlflow API.
"""

import os
from typing import Dict

import mlflow

from pii_recognition.constants import BASE_DIR

DEFAULT_TRACKER_URI = os.path.join(BASE_DIR, "mlruns")


def _get_experiment_id(experiment_name: str):
    return mlflow.get_experiment_by_name(experiment_name).experiment_id


def start_tracker(
    experiment_name: str,
    run_name: str = "default",
    tracker_uri: str = DEFAULT_TRACKER_URI,
):
    mlflow.set_tracking_uri(tracker_uri)

    # create experiments at tracker_uri
    mlflow.set_experiment(experiment_name)

    experiment_id = _get_experiment_id(experiment_name)
    mlflow.start_run(run_name=run_name, experiment_id=experiment_id)


def end_tracker():
    mlflow.end_run()


def log_metric_per_entity(metric: Dict[str, float], metric_name: str = None):
    for entity_name, entity_score in metric.items():
        mlflow.log_metric(entity_name + f"_{metric_name}", entity_score)
