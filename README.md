# Personal Identifiable Information (PII) Recognition
This project is still under development and will be going through several stages.

The first stage is to build a benchmark model. We have chosen `CRF` for benchmarking, for a couple of reasons. PII recognition in fact is a sequential labelling problem where you are predicting a series of PII labels on a provided sequence, with the labels in hand you can do anonymization. `CRF` has made reasonable assumptions just to solve this sequence labelling type of problems. `CRF` is also the foundation of many complex models, knowing its behaviour would help understand of many other models. The most important reason to explore `CRF` is that inference is fast on `CRF`, with all of the models being tested, `CRF` championed on speed, second best option other than regex if you value speed a lot. The challenge of `CRF` lies in feature engineering, you have to be creative to build your own features or use deep learning to automate feature extraction. This motivate us to take a look of SOTA models, mostly deep learning based.

The second stage is to evaluate as many as off-the-shelf NER models and find the most promising one/ones. We assume NER is the superset of PII, solving NER is equivalent to solving PII. Evaluation focuses on the conventional metrics of `recall`, `precision`, `f1` and inference time as well. Complex NER models like `Flair` did achieve superior scores across many of its supported entities, but inference is very very slow if GPU and batch both are disabled. `Spacy` models have shown us a good balance -- decent scores with quick inference. But its downside is obvious, same as all of the off-the-shelf models tested, it lacks the ability to be extended on new entities unless retrain the model. Another problem with these models is that there is no consensus on the definition of an entity. For example, `LOC` in Spacy `xx_ent_wiki_sm` model means `LOC` and `GPE` in Spacy `en_core_web_lg` model.

Moving forward we will focus on regex and anonymization. Regex is the enhancement of building bespoke model handling a particular type of entity, for example, medicare number in Australia. Anonymization is about redaction and demoing the final work in which end-users would see.

## Installation
The project is developed with Python3.7, make sure you it available. Other versions of Python may work, but you may have to downgrade specific libraries to fix compatibility issues.

Installing `poetry`, a tool that gracefully handles dependencies for you.
```
pip install poetry
```
Using `install` command to download and install required dependencies listed in `poetry.lock`. This could take a while.
```
poetry install
```

If you want to create virtualenv inside the project's root directory, you can update `poetry` config.
```
poetry config virtualenvs.in-project true
```
Starting a shell and you are ready
```
poetry shell
```

## Quick Start

### Example Usage
#### CRF Model
Load a pretrained CRF model and fire up the analyser.

```python
from pii_recognition.recognisers.crf_recogniser import CrfRecogniser

crf_recogniser = CrfRecogniser(
    supported_entities=["I-LOC", "I-ORG", "I-PER", "I-MISC"],
    supported_languages=["en"],
    model_path="pii_recognition/exported_models/conll2003-en.crfsuite",
    tokeniser_setup={"name": "TreebankWordTokeniser"},
)

crf_recogniser.analyse(text="I love Melbourne.", entities=["I-PER", "I-LOC"])
```

You will get span labels as follows
```console
[SpanLabel(entity_type='I-LOC', start=7, end=16)]
```


#### spaCy Model
Create a spaCy recogniser and kick off the analyser.

```python
from pii_recognition.recognisers.spacy_recogniser import SpacyRecogniser

spacy_recogniser = SpacyRecogniser(
    supported_entities=["LOC", "MISC", "ORG", "PER"],
    supported_languages=["en", "de", "es", "fr", "it", "pt", "ru"],
    model_name="xx_ent_wiki_sm",
)
spacy_recogniser.analyse(text="I love Melbourne.", entities=["PER", "LOC"])
```

You will get span labels as follows
```console
[SpanLabel(entity_type='LOC', start=7, end=16)]
```

#### Other available models
Many other off-the-shelf models are provided as well with the detail implementations found in `recognisers` folder, including two neural networks based inference models [`flair`](https://github.com/flairNLP/flair) and [`stanza`](https://github.com/stanfordnlp/stanza).


## Train a Recogniser
Training is not the focus for this project. Two directories, `features` and `exported_models`, have been maintained for training as it is needed for developing CRF models and should be aware that files within are not tested.

## Evaluate a Recogniser
### Evaluation Dataset Format
Evaluation requires sentences to be the *input*.
```python
input_data: List[str] = ["A sentence to be evaluated.", "I love Melbourne."]
```

*Ground truth* is assigned at a token-level for each input sentence. Each token of the sentence will be assigned with an entity label. The label could be in either BIO schema or IO schema.
```python
ground_truths = [["O", "O", "O", "O", "O", "O"], ["O", "O", "I-LOC", "O"]]
```

### Evaluator
Evaluation is measured by `recall`, `precision` and `f-score`. Evaluator takes a recogniser and evaluate over a given dataset.

### Build Pipeline with Pakkr + MLflow
Pakkr is an awesome lightweight tool published by Zendesk ML team for pipeline development. MLflow Tracking is an API to log results and parameters in machine learning experiments and report them in an interactive UI.


The experiments have been put at `pii_recognition/experiments/` folder, you can pick one and test the pipeline out by executing the following. Note, batch and GPU are not supported yet, evaluating over deep learning models would be slow.
```
python pii_recognition/pipelines/pakkr_evaluation.py --config_yaml pii_recognition/experiments/you_pick
```

MLflow Tracking will log the run and the interaction UI is available at http://localhost:5000. Start it with:
```
mlflow ui
```

### Performance
Evaluation of experiments are performed on CONLL 2003 English data -- `eng.testb` with `MLflow` on `f1`, `precision` and `recall`. We will be updating the table as the project moves forward.


| Experiment | Run | Test Set | Recall | Precision | F1 |  Evaluation Duration |
| -------------    | ------------- |------------- |------------- |------------- |------------- |------------- |
| Heuristic | first_letter_uppercase |  Conll-03 en.testb  |  0.973 | 0.298| 0.456| 1.1s   |
| CRF       | python_crf_no_pos      |  Conll-03 en.testb  |  0.887 | 0.824| 0.854| 1.4s   |
| Spacy     | en_core_web_lg         |  Conll-03 en.testb  |  0.824 | 0.828| 0.826| 6.7s   |
|           | xx_ent_wiki_sm         |  Conll-03 en.testb  |  0.764 | 0.789| 0.776| 6.9s   |
|Flair      | pretrained_en          |  Conll-03 en.testb  |  0.986 | 0.980| 0.983| 32.6min|
|Stanza     | pretrained_en          |  Conll-03 en.testb  |  0.855 | 0.846| 0.850| 10.6min|

notes: no batch is enabled, all models are running on CPU and tested with English dataset on PERSON entity
