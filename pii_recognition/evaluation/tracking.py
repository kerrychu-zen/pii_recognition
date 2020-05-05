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


def start_tracker(experiment_name: str, run_name: str, artifact_location: str):
    # TODO: add test
    try:
        mlflow.create_experiment(
            name=experiment_name, artifact_location=artifact_location
        )
    except MlflowException:
        logging.info(f"Experiment {experiment_name} already exists.")

    mlflow.start_run(run_name=run_name)


def end_tracker():
    # TODO: add test
    mlflow.end_run()


def track_evaluation(
    evaluator: ModelEvaluator,
    X_test: List[str],
    y_test: List[List[str]],
    experiment_name: Optional[str] = None,
    run_name: str = "default",
    f_beta: float = 1.0,
):
    recogniser = evaluator.recogniser
    tokeniser = evaluator.tokeniser

    if experiment_name is None:
        experiment_name = recogniser.name

    artifact_path = os.path.join(BASE_DIR, "artifacts", f"{experiment_name}")
    activate_experiment(experiment_name, artifact_path)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name):
        counters, mistakes = evaluator.evaulate_all(X_test, y_test)

        recall, precision, f_score = evaluator.calculate_score(counters, f_beta)

        with tempfile.TemporaryDirectory() as tempdir:
            output_file = os.path.join(tempdir, f"{run_name}.mistakes")
            write_iterable_to_text(mistakes, output_file)
            mlflow.log_artifact(output_file)

        log_metrics(recall, suffix="recall")
        log_metrics(precision, suffix="precision")
        log_metrics(f_score, suffix="f1")

        mlflow.log_param("supported_languages", recogniser.supported_languages)
        mlflow.log_param("supported_entities", recogniser.supported_entities)
        mlflow.log_param("tokeniser", tokeniser.__name__)


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
