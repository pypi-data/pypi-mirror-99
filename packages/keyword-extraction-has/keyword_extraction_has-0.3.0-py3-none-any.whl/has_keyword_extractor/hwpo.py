from typing import Dict


def compute_hwpo(bigram: str, bigram_frequency: Dict, cumul_bigram: Dict):
    if bigram not in bigram_frequency:
        return -100
    key_max = max(list(cumul_bigram.keys()))
    return cumul_bigram[bigram_frequency[bigram]] / cumul_bigram[key_max]
