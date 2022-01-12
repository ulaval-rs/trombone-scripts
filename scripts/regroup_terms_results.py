"""
Ce script permet de combiner les résultats du script `find_terms_frequency.py`.
Ce dernier trouve la fréquence des termes par document, et les ajoute à un fichier csv.
Ce script, `regroup_terms_results.py`, combine les résultats pour tous les documents
pour obtenir les résultats pour le corpus.
"""
import getopt
import os
import sys

import pandas
from pytrombone import Cache

CSV_FILEPATH = ''
CACHE_PATH = ''
ALL_TERMS_FILEPATH = ''


# Récupération des arguments
optlist, _ = getopt.getopt(sys.argv[1:], '', ['csv_file=', 'cache_path=', 'all_terms_filepath='])

for opt, value in optlist:
    if 'csv_file' in opt:
        CSV_FILEPATH = value

    if 'cache_path' in opt:
        CACHE_PATH = value

    if 'all_terms_filepath' in opt:
        ALL_TERMS_FILEPATH = value

if not CSV_FILEPATH or not CACHE_PATH or not ALL_TERMS_FILEPATH:
    raise ValueError('Les paramètres csv_file, cache_path et all_terms_filepath doivent tous être fournies')

# Récupération des termes de tous les documents
df = pandas.read_csv(ALL_TERMS_FILEPATH)

unique_terms = df['term'].unique()
unique_documents = df['filename'].unique()

nbr_of_terms = len(unique_terms)
nbr_of_documents = len(unique_documents)

# Finding total number of terms
total_number_of_terms = 0
for document in unique_documents:
    document_rows = df.loc[df['filename'] == document]
    total_number_of_terms += len(document_rows)

# Initialisation de la cache, qui marque si oui ou non un terme à été traité
cache = Cache(CACHE_PATH)

for term in unique_terms:
    term = str(term)

    # On ignore les termes qui ne sont que des chiffres.
    if not term.isalpha():
        # Marque le terme comme traité
        cache.mark_as_processed(term)
        continue

    # Vérifie que le terme n'a pas déjà été traité
    if cache.has_been_processed(term):
        continue

    # On trouve toutes les occurrences des termes par document.
    term_rows = df.loc[df['term'] == term]
    term_df = pandas.DataFrame(data={
        'Term': [term],
        'TotalOccurrences': [sum(term_rows['rawFreq'])],
        'RelativeOccurrencesInAllDocument': [sum(term_rows['rawFreq']) / total_number_of_terms],

        'AverageOccurrencesPerDocument': [sum(term_rows['rawFreq']) / nbr_of_documents],
        'AverageRelativeOccurrencesPerDocument': [sum(term_rows['relativeFreq']) / nbr_of_documents / 1_000_000],  # Pour obtenir une valeur normalisée

        'DocumentsWhereTermIsPresentCount': [len(term_rows['filename'].unique())],
        'TotalTermsCount': [nbr_of_terms],
        'TotalDocumentsCount': [nbr_of_documents],
    })

    # Écriture dans un fichier csv
    if os.path.exists(CSV_FILEPATH):
        term_df.to_csv(CSV_FILEPATH, mode='a', header=False, index=False)

    else:
        term_df.to_csv(CSV_FILEPATH, index=False)

    # Marque le terme comme traité
    cache.mark_as_processed(term)
