import click
import spacy
from has_keyword_extractor.utils import parse_files
from has_keyword_extractor._runner import st_process_doc, st_process_multiple_doc


@click.group()
def doc():
    pass


@doc.command()
@click.option("--alpha", required=True, type=float)
@click.option("--spacy-model", required=True)
@click.option("--threshold", required=True, type=float)
@click.option("--path", required=True)
def process_doc(path, spacy_model, alpha, threshold):
    nlp = spacy.load(spacy_model)
    text = '\n'.join(open(path, 'r').readlines())
    print(st_process_doc(text, nlp, alpha, threshold))


@click.group()
def docs():
    pass


@doc.command()
@click.option("--alpha", required=True, type=float)
@click.option("--spacy-model", required=True)
@click.option("--threshold", required=True, type=float)
@click.option("--path", required=True)
def process_docs(path, spacy_model, threshold, alpha):
    nlp = spacy.load(spacy_model)
    documents = parse_files(path)
    print(st_process_multiple_doc(documents, nlp, alpha, threshold))


keyword_extractor = click.CommandCollection(sources=[doc, docs])
if __name__ == '__main__':
    keyword_extractor()
