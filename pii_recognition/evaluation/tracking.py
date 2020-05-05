import logging
import os
import tempfile
from typing import Any, Dict, List, Optional

import mlflow
from mlflow.exceptions import MlflowException

from pii_recognition.constants import BASE_DIR
from pii_recognition.evaluation.model_evaluator import ModelEvaluator
from pii_recognition.recognisers.entity_recogniser import EntityRecogniser


def start_tracker(experiment_name: str, run_name: str = "default"):
    artifact_location = os.path.join(BASE_DIR, "artifacts", f"{experiment_name}")

    try:
        mlflow.create_experiment(
            name=experiment_name, artifact_location=artifact_location
        )
    except MlflowException:
        mlflow.set_experiment(experiment_name)
        logging.info(f"Experiment {experiment_name} already exists.")

    experiment_id = get_experiment_id(experiment_name)
    mlflow.start_run(run_name=run_name, experiment_id=experiment_id)


def get_experiment_id(experiment_name: str):
    # TODO: add test
    return mlflow.get_experiment_by_name(experiment_name).experiment_id


def end_tracker():
    # TODO: add test
    mlflow.end_run()


def log_metric_per_entity(metric: Dict[str, float], metric_name: str = None):
    for entity_name, entity_score in metric.items():
        mlflow.log_metric(entity_name + f"_{metric_name}", entity_score)
