import statistics
from typing import Counter, Dict


def compute_cumul_freq_monogram(monogram_frequencies: Counter) -> Dict:
    monogram_cumul_freqs = {}
    for freq in monogram_frequencies.values():
        if freq not in monogram_cumul_freqs.keys():
            monogram_cumul_freqs[freq] = 1
        monogram_cumul_freqs[freq] += 1

    monogram_cumul_freqs = {
        freq_key: statistics.mean(
            [
                cumul_freq_value
                for other_freq_key, cumul_freq_value in monogram_cumul_freqs.items()
                if other_freq_key != freq_key
            ]
        )
        for freq_key in monogram_cumul_freqs
    }
    cumul = 0
    for key in sorted(list(monogram_cumul_freqs.keys())):
        cumul += monogram_cumul_freqs[key]
        monogram_cumul_freqs[key] = cumul

    return monogram_cumul_freqs


def compute_cumul_freq_bigram(bigram_frequencies: Counter):
    bigram_cumul_freqs = {}
    for freq in bigram_frequencies.values():
        if freq not in bigram_cumul_freqs.keys():
            bigram_cumul_freqs[freq] = 1
        bigram_cumul_freqs[freq] += 1
    bigram_cumul_freqs[1] = statistics.mean(
        [
            cumul_value
            for freq_key, cumul_value in bigram_cumul_freqs.items()
            if freq_key != 1
        ]
    )
    cumul = 0
    for key in sorted(list(bigram_cumul_freqs.keys())):
        cumul += bigram_cumul_freqs[key]
        bigram_cumul_freqs[key] = cumul
    return bigram_cumul_freqs
