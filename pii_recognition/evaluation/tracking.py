import logging
import os
import tempfile
from typing import Any, Dict, List, Optional

import mlflow
from mlflow.exceptions import MlflowException

from constants import BASE_DIR, LABEL_COMPLIANCE
from evaluation.model_evaluator import ModelEvaluator
from recognisers.entity_recogniser import EntityRecogniser
from utils import write_iterable_to_text


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


def log_metrics(metrics: Dict, suffix: Optional[str] = None):
    # TODO: add test!
    for key, value in metrics.items():
        assert isinstance(key, str), f"Metric key must be string but got {type(key)}"

        if key in LABEL_COMPLIANCE:
            if suffix:
                key_name = LABEL_COMPLIANCE[key] + f"_{suffix}"
            else:
                key_name = LABEL_COMPLIANCE[key]
        else:
            if suffix:
                key_name = key + f"_{suffix}"
            else:
                key_name = key

        mlflow.log_metric(key_name, value)


def log_params(params: Dict[str, Any]):
    # TODO: add test!
    for key, value in params.items():
        if callable(value):
            mlflow.log_param(key, value.__name__)
        elif isinstance(value, list):
            mlflow.log_param(key, ", ".join(map(str, value)))
        else:
            mlflow.log_param(key, value)
