import random
import unittest

from kolibri.data.text.corpus import ConsumerComplaintsCorpus
from kolibri.dnn.utils import load_data_object
from kolibri.indexers import SequenceCharIndexer
from kolibri.tokenizer import WordTokenizer

tokenizer = WordTokenizer()


class TestSequenceIndexer(unittest.TestCase):
    def test_text_indexer(self):
        corpus = ConsumerComplaintsCorpus()
        x_set, y_set = corpus.get_data(nb_samples=50)
        x_set = tokenizer.transform(x_set)
        x_samples = random.sample(x_set, 5)
        text_indexer = SequenceCharIndexer(min_count=1)
        text_indexer.build_vocab(x_set, y_set)
        text_idx = text_indexer.transform(x_samples)

        text_info_dict = text_indexer.to_dict()
        text_indexer2 = load_data_object(text_info_dict)

        text_idx2 = text_indexer2.transform(x_samples)

        for i, idx in enumerate(text_idx):
            assert (idx == text_idx2[i]).all()


if __name__ == "__main__":
    pass
