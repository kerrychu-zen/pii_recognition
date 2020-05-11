from pathlib import PurePath
from typing import List, Tuple, Set

from nltk.corpus.reader import ConllCorpusReader

from pii_recognition.tokenisation.detokenisers import Detokeniser

from .reader import Data, Reader


def _sent2tokens(sent: List[Tuple[str, str, str]]) -> List[str]:
    return [token for token, postag, label in sent]


def _sent2labels(sent: List[Tuple[str, str, str]]) -> List[str]:
    return [label for token, postag, label in sent]


class ConllReader(Reader):
    def __init__(self, detokeniser: Detokeniser):
        self._detokeniser = detokeniser

    def _get_corpus(self, file_path: str) -> ConllCorpusReader:
        path = PurePath(file_path)
        return ConllCorpusReader(
            root=str(path.parents[0]),
            fileids=str(path.name),
            columntypes=["words", "pos", "ignore", "chunk"],
        )

    def get_test_data(
        self, file_path: str, supported_entities: List[str], is_io_schema: bool = True
    ) -> Data:
        """
        Read CONLL type of data.
        """
        data = self._get_corpus(file_path)

        sent_features = list(data.iob_sents())
        sent_features = [x for x in sent_features if x]  # remove empty features

        labels = []
        sents = []
        for sent_feat in sent_features:
            sent_labels = _sent2labels(sent_feat)
            self._validate_entity(set(sent_labels), set(supported_entities))
            sent_str = self._detokeniser.detokenise(_sent2tokens(sent_feat))
            labels.append(sent_labels)
            sents.append(sent_str)

        return Data(sents, labels, supported_entities, is_io_schema,)
