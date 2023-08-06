import warnings
from collections import Counter
from typing import Dict

import nltk

from has_keyword_extractor.compute_cumulative_frequencies import (
    compute_cumul_freq_monogram,
    compute_cumul_freq_bigram,
)
from has_keyword_extractor.fbi import compute_fbi
from has_keyword_extractor.fni import compute_fni
from has_keyword_extractor.hwo import compute_hwo
from has_keyword_extractor.hwpo import compute_hwpo
from has_keyword_extractor.ranked_ngrams import compute_ranked_ngrams


class StatisticsKeywordsExtraction:
    def __init__(self, words: list[str], alpha: float, threshold: float):
        self.words = words
        self.bigrams = list(nltk.bigrams(words))
        self.bigram_frequencies = Counter(
            i for i in filter(lambda x: "[PUNCT]" not in x, self.bigrams)
        )
        self.monogram_frequencies = Counter(filter(lambda x: x != "[PUNCT]", words))
        self.alpha = alpha
        self.threshold = threshold

    def extract_keywords(self) -> Dict:

        if (
            len(set(self.monogram_frequencies.values())) < 3
            or len(set(self.bigram_frequencies.values())) < 3
        ):
            warnings.warn(
                "it seems that the documents is too short to apply this method 😢. "
                "No keywords could be returned may be "
                "you could just indexed all the content instead ? "
            )
            return {
                "top_ranked_bigrams": [],
                "highest_monogram": [],
                "highest_ngrams": [],
                "top_ranked_ngram": [],
            }

        cumul_monogram = compute_cumul_freq_monogram(self.monogram_frequencies)
        cumul_bigram = compute_cumul_freq_bigram(self.bigram_frequencies)

        hwo_bow = {
            word: compute_hwo(word, self.monogram_frequencies, cumul_monogram)
            for word in self.words
        }

        hwpo_bow = {
            bigram: compute_hwpo(bigram, self.bigram_frequencies, cumul_bigram)
            for bigram in list(self.bigram_frequencies)
        }

        no_filtered_bigrams = compute_fbi(
            self.bigram_frequencies, hwpo_bow, hwo_bow, self.alpha
        )

        fni_ngrams = compute_fni(no_filtered_bigrams, self.threshold)

        return compute_ranked_ngrams(
            fni_ngrams, self.bigram_frequencies, self.monogram_frequencies
        )
