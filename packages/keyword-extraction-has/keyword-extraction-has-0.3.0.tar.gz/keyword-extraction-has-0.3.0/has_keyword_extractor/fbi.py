def compute_fbi(bigrams_frequencies, hwpo_bow, hwo_bow, alpha):
    fbi_grams = {
        bigram: hwpo_bow[bigram]
        * (1 - (alpha * (hwo_bow[bigram[0]] + hwo_bow[bigram[1]])))
        for bigram in bigrams_frequencies
    }
    return fbi_grams
