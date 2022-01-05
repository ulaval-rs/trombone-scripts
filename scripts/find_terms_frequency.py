"""
Ce script obtient la fréquence des termes de document individuel,
et les combines en un seul fichier csv
"""
import getopt
import json
import os
import sys
from typing import Dict, List

import pandas

from pytrombone import Trombone, Cache, filepaths_loader

PDFS_PATH_PATTERN = ''
CSV_FILEPATH = ''
CACHE_PATH = ''

# Récupération des arguments
optlist, _ = getopt.getopt(sys.argv[1:], '', ['pdfs_path_pattern=', 'csv_file=', 'cache_path='])

for opt, value in optlist:
    if 'pdfs_path_pattern' in opt:
        PDFS_PATH_PATTERN = value

    if 'csv_file' in opt:
        CSV_FILEPATH = value

    if 'cache_path' in opt:
        CACHE_PATH = value

if not PDFS_PATH_PATTERN or not CSV_FILEPATH or not CACHE_PATH:
    raise ValueError('Les paramètres pdfs_path_pattern, csv_file et cache_path doivent tous être fournies')

trombone = Trombone()
cache = Cache(CACHE_PATH)


def make_series_from_dict(data: Dict, name: str) -> pandas.Series:
    return pandas.Series(
        data=data[name],
        index=data[name].keys(),
        name=name,
    )


def transform_terms_result_to_dataframe(filename: str, result: Dict) -> pandas.DataFrame:
    terms: List[Dict] = result['documentTerms']['terms']
    for term in terms:
        term['filename'] = filename

    df = pandas.DataFrame.from_records(terms)

    # Retrait de valeurs inutiles
    df = df.drop(['docIndex', 'docId'], axis=1)

    return df


for filepaths in filepaths_loader(PDFS_PATH_PATTERN, batch_size=1, cache=cache):
    filenames = [os.path.basename(f) for f in filepaths]
    if not filenames:
        continue

    # Parce qu'on utilise une batch_size=1
    filename = filenames[0]

    key_values = [
        ('tool', 'corpus.DocumentTerms'),
        ('storage', 'file'),  # Stock les textes dans des fichiers en cache plutôt que d'utiliser la mémoire vive
        ('minRawFreq', 5)
    ]
    # Ajout des fichiers à analyser
    key_values += [('file', filepath) for filepath in filepaths]

    try:
        output, error = trombone.run(key_values)
        output = trombone.serialize_output(output)

    except json.JSONDecodeError:
        cache.mark_as_failed(filename)
        continue

    if not output['documentTerms']['terms']:
        cache.mark_as_failed(filename)
        continue


    results = transform_terms_result_to_dataframe(filename, output)

    # Écriture dans un fichier csv
    if os.path.exists(CSV_FILEPATH):
        results.to_csv(CSV_FILEPATH, mode='a', header=False, index=False)

    else:
        results.to_csv(CSV_FILEPATH, index=False)

    cache.mark_as_processed(filenames)
