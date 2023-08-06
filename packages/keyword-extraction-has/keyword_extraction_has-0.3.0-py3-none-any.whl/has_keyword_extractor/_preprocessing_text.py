import re


def preprocessing_text(text: str, nlp, sep="[PUNCT]") -> list[str]:
    text = re.sub(r"\d+", "", text).lower()
    # tokenize text
    doc = nlp(text)
    # remove stopwords
    words_list = []

    for token in doc:
        if token.is_punct or token.is_stop:
            words_list.append(sep)
        elif not token.is_space:
            words_list.append(token.lemma_)
    return words_list
