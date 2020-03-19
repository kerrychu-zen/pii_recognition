import mlflow

from data_reader.conll_reader import get_conll_eval_data
from evaluation.model_evaluator import ModelEvaluator
from recognisers.spacy_recogniser import SpacyRecogniser
from tokeniser.detokeniser import space_join_detokensier
from tokeniser.tokeniser import nltk_word_tokenizer
from utils import write_iterable_to_text

from .manage_experiments import Spacy_EXP

RUN_NAME = "xx_ent_wiki_sm"

recogniser = SpacyRecogniser(
    supported_entities=["LOC", "MISC", "ORG", "PER"],
    supported_languages=["en", "de", "es", "fr", "it", "pt", "ru"],
    model_name="xx_ent_wiki_sm",
)


# Prepare evalution data
X_test, y_test = get_conll_eval_data(
    file_path="datasets/conll2003/eng.testb", detokenizer=space_join_detokensier
)


# Log to mlflow
mlflow.set_experiment(Spacy_EXP)
with mlflow.start_run(run_name=RUN_NAME):
    evaluator = ModelEvaluator(
        recogniser, ["PER"], nltk_word_tokenizer, to_eval_labels={"PER": "I-PER"}
    )

    counters, mistakes = evaluator.evaulate_all(X_test, y_test)
    # remove returns with no mistakes
    mistakes = list(filter(lambda x: x.token_errors, mistakes))
    recall, precision, f1 = evaluator.calculate_score(counters, f_beta=1.0)
    _, _, f2 = evaluator.calculate_score(counters, f_beta=2.0)

    write_iterable_to_text(mistakes, f"{RUN_NAME}.mis")
    mlflow.log_artifact(f"{RUN_NAME}.mis")

    mlflow.log_metric("PER_recall", recall["I-PER"])
    mlflow.log_metric("PER_precision", precision["I-PER"])
    mlflow.log_metric("PER_f1", f1["I-PER"])
    mlflow.log_metric("PER_f2", f2["I-PER"])
