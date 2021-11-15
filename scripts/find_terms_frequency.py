"""
Ce script obtient la fréquence des termes de document individuel,
et les combines en un seul fichier csv
"""
import json
import os
from typing import Dict, List

import pandas

from trombone import Trombone
from trombone.cache import Cache
from trombone.loader import path_loader_batch

PDFS_PATH = '../data/pdfs'
CSV_FILEPATH = '../data/terms.csv'
CACHE_PATH = '../data/cache-terms.db'

trombone = Trombone('../bin/trombone-5.2.1-SNAPSHOT-jar-with-dependencies.jar')
cache = Cache(CACHE_PATH)


def make_series_from_dict(data: Dict, name: str) -> pandas.Series:
    return pandas.Series(
        data=data[name],
        index=data[name].keys(),
        name=name,
    )


def transform_terms_result_to_dataframe(result: Dict) -> pandas.DataFrame:
    terms: List[Dict] = result['documentTerms']['terms']
    df = pandas.DataFrame.from_records(terms)

    # Retrait de valeurs inutiles
    df = df.drop(['docIndex', 'docId'], axis=1)

    return df



for filepaths, filenames in path_loader_batch('../tests/data/pdfs/*_E.pdf', batch_size=1, cache=cache):
    if not filenames:
        continue

    key_values = [
        ('tool', 'corpus.DocumentTerms'),
        # ('tool', 'corpus.CorpusTerms'),
        ('storage', 'file'),  # Stock les textes dans des fichiers en cache plutôt que d'utiliser la mémoire vive
    ]
    # Ajout des fichiers à analyser
    key_values += [('file', filepath) for filepath in filepaths]

    try:
        output, error = trombone.run(key_values)
        output = trombone.serialize_output(output)

    except json.JSONDecodeError:
        cache.mark_as_failed(filenames)
        continue

    if not output['documentTerms']['terms']:
        cache.mark_as_failed(filenames)
        continue

    results = transform_terms_result_to_dataframe(output)

    # Écriture dans un fichier csv
    if os.path.exists(CSV_FILEPATH):
        results.to_csv(CSV_FILEPATH, mode='a', header=False, index=False)

    else:
        results.to_csv(CSV_FILEPATH, index=False)

    cache.mark_as_processed(filenames)
