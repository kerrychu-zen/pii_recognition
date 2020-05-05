import logging
import os
import tempfile
from typing import Any, Dict, List, Optional

import mlflow
from mlflow.exceptions import MlflowException

from pii_recognition.constants import BASE_DIR
from pii_recognition.evaluation.model_evaluator import ModelEvaluator
from pii_recognition.recognisers.entity_recogniser import EntityRecogniser


def start_tracker(experiment_name: str, run_name: str):
    # TODO: add test
    artifact_location = os.path.join(BASE_DIR, "artifacts", f"{experiment_name}")

    try:
        mlflow.create_experiment(
            name=experiment_name, artifact_location=artifact_location
        )
    except MlflowException:
        mlflow.set_experiment(experiment_name)
        logging.info(f"Experiment {experiment_name} already exists.")

    mlflow.start_run(run_name=run_name)


def end_tracker():
    # TODO: add test
    mlflow.end_run()


def log_metric_per_entity(metric: Dict[str, float], metric_name: str = None):
    for entity_name, entity_score in metric.items():
        mlflow.log_metric(entity_name + f"_{metric_name}", entity_score)
