from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict

from alive_progress import alive_bar
from has_keyword_extractor._preprocessing_text import preprocessing_text
from has_keyword_extractor._statistics_keywords_extraction import StatisticsKeywordsExtraction


def st_process_doc(text: str, nlp, alpha: float, threshold: float):
    return StatisticsKeywordsExtraction(
        preprocessing_text(text, nlp), alpha, threshold
    ).extract_keywords()


def st_process_multiple_doc(
    documents: Dict[str, str], nlp, alpha: float, threshold: float, workers=20
):
    print("🔎 Begin keyword extraction : ")
    result = {}
    with alive_bar(
        len(documents), title="number of processed documents", length=100
    ) as progress_bar:
        with ThreadPoolExecutor(workers) as executor:
            future_to_url = {
                executor.submit(st_process_doc, content, nlp, alpha, threshold): title
                for title, content in documents.items()
            }
            for future in futures.as_completed(future_to_url):
                result[future_to_url[future]] = future.result()
                progress_bar()
    print("keyword extraction is ended")
    return result
