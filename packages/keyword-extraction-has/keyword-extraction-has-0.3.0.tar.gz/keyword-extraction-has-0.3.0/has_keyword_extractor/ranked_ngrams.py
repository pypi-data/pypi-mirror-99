import statistics


def compute_ranked_ngrams(fni_ngrams, bigram_frequencies, monogram_frequencies, sep='[PUNCT]'):
    highest_ngrams_freqs = sorted(
        dict(
            filter(lambda x: sep not in x[0], bigram_frequencies.items())
        ).items(),
        key=lambda x: x[1],
        reverse=True,
    )[0][1]
    highest_monogram = extract_high_relevant_monograms(
        monogram_frequencies, highest_ngrams_freqs
    )
    top_ranked_bigram = sorted(fni_ngrams[0], key=lambda x: x[1], reverse=True)[:11]
    top_bigram_mean = statistics.mean(bigram[1] for bigram in top_ranked_bigram)
    ngrams = [ngram for ngrams in fni_ngrams[1:] for ngram in ngrams if ngram[1]]
    highest_ngrams = [
        ngram
        for ngrams in fni_ngrams[1:]
        for ngram in ngrams
        if ngram[1] >= top_bigram_mean
    ]
    top_ranked_ngram = sorted(ngrams, key=lambda x: x[1], reverse=True)[:11]

    return {
        "top_ranked_bigrams": top_ranked_bigram,
        "highest_monogram": highest_monogram,
        "highest_ngrams": highest_ngrams,
        "top_ranked_ngram": top_ranked_ngram,
    }


def extract_high_relevant_monograms(monograms, highest_ngrams_freqs, sep="[PUNCT]"):
    high_relevant_monograms = []
    for gram in monograms.items():
        if gram[1] > highest_ngrams_freqs * 8 and gram[0] != sep:
            high_relevant_monograms.append(gram)
    return high_relevant_monograms
