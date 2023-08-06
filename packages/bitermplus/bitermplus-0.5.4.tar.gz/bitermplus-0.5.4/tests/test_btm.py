import bitermplus as btm
import unittest
import os.path
import sys
import numpy as np
import logging
from gzip import open as gzip_open
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
LOGGER = logging.getLogger(__name__)


class TestBTM(unittest.TestCase):

    # Plotting tests
    def test_btm_class(self):
        with gzip_open('dataset/SearchSnippets.txt.gz', 'rb') as file:
            texts = file.readlines()

        X, vocab = btm.util.get_words_freqs(texts)
        docs_vec = btm.util.get_vectorized_docs(X)
        biterms = btm.util.get_biterms(X)

        LOGGER.info('Modeling started')
        model = btm.BTM(X, T=8, W=vocab.size, M=20, alpha=50/8, beta=0.01)
        # t1 = time.time()
        model.fit(biterms, iterations=20)
        # t2 = time.time()
        # LOGGER.info(t2 - t1)
        LOGGER.info('Modeling finished')

        self.assertIsInstance(model.matrix_words_topics_, np.ndarray)
        self.assertTupleEqual(model.matrix_words_topics_.shape, (8, vocab.size))
        p_zd = model.transform(docs_vec)

        LOGGER.info('Perplexity started')
        perplexity = btm.metrics.perplexity(model.matrix_words_topics_, p_zd, X, 8)
        self.assertIsInstance(perplexity, float)
        self.assertNotEqual(perplexity, 0.)
        LOGGER.info('Perplexity finished')

        LOGGER.info('Coherence started')
        coherence = btm.metrics.coherence(model.matrix_words_topics_, X, M=20)
        self.assertIsInstance(coherence, np.ndarray)
        self.assertGreater(coherence.shape[0], 0)
        LOGGER.info('Coherence finished')


if __name__ == '__main__':
    unittest.main()
