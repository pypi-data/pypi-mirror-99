import itertools
import statistics


def recursive_fbi_extraction(ngrams, threshold, sep="[PUNCT]"):
    last_ngram = ngrams[-1]
    conserved_ngram = ngrams[-1]
    trigram = []
    ngram_it = iter(last_ngram)
    for (bigram, score) in ngram_it:
        next_bigram, next_score = next(ngram_it, (None, None))
        if next_bigram is None:
            break
        if bigram[1] == next_bigram[0]:
            if next_score > threshold and score > threshold:
                trigram.append(
                    (
                        tuple(list(bigram) + [next_bigram[-1]]),
                        statistics.mean([score, next_score]),
                    )
                )
                conserved_ngram.remove((bigram, score))
                conserved_ngram.remove((next_bigram, next_score))
        else:
            ngram_it = itertools.chain(ngram_it, [(next_bigram, next_score)])

    ngrams[-1] = [ngram for ngram in conserved_ngram if sep not in ngram[0]]
    ngrams.append(trigram)
    if trigram:
        recursive_fbi_extraction(ngrams, sep)
    return ngrams[:-1]


def compute_fni(fbi_bigrams, threshold, sep="[PUNCT]"):
    return recursive_fbi_extraction([list(fbi_bigrams.items())], threshold, sep)
