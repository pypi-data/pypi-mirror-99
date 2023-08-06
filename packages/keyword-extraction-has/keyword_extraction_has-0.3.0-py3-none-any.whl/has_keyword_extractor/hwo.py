from typing import Dict


def compute_hwo(word: str, monogram_frequency: Dict, cumul_monogram: Dict):
    if word not in monogram_frequency:
        return -100
    key_max = max(list(cumul_monogram.keys()))
    return cumul_monogram[monogram_frequency[word]] / cumul_monogram[key_max]
