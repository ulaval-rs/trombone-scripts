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

CSV_FILEPATH = ''
ALL_TERMS_FILEPATH = ''

# Récupération des arguments
optlist, _ = getopt.getopt(sys.argv[1:], '', ['csv_file=', 'all_terms_filepath='])

for opt, value in optlist:
    if 'csv_file' in opt:
        CSV_FILEPATH = value

    if 'all_terms_filepath' in opt:
        ALL_TERMS_FILEPATH = value

if not CSV_FILEPATH or not ALL_TERMS_FILEPATH:
    raise ValueError('Les paramètres csv_file et all_terms_filepath doivent tous être fournies')


df = pandas.read_csv(ALL_TERMS_FILEPATH)

new_df = pandas.DataFrame(
    columns=['term', 'totalRawFreq', 'relativeFreqAvg', 'zscoreAvg', 'zscoreRatioAvg', 'tfidfAvg', 'totalTermsCount']
)
terms_without_duplicates = ()

# Lit le fichier de résultats des termes regroupé (s'il existe, ici le fichier agit en tant que cache)
if os.path.exists(CSV_FILEPATH):
    already_processed_terms = pandas.read_csv(CSV_FILEPATH)
else:
    already_processed_terms = None

for term in df['term'].unique():
    # On ignore les termes qui ne sont que des chiffres.
    if not term.isalpha():
        continue

    if already_processed_terms is not None:
        if term in already_processed_terms['term'].values:
            continue

    # On trouve toutes les occurrences des termes par document.
    term_rows = df.loc[df['term'] == term]
    new_df = new_df.append({
        'term': term,
        'totalRawFreq': sum(term_rows['rawFreq']),
        'relativeFreqAvg': sum(term_rows['relativeFreq']) / len(term_rows['relativeFreq']) / 1_000_000, # Pour obtenir une valeur normalisée
        'zscoreAvg': sum(term_rows['zscore']) / len(term_rows['zscore']),
        'zscoreRatioAvg': sum(term_rows['zscoreRatio']) / len(term_rows['zscoreRatio']),
        'tfidfAvg': sum(term_rows['tfidf']) / len(term_rows['tfidf']),
        'totalTermsCount': sum(term_rows['totalTermsCount']),
    }, ignore_index=True)

    # Écriture dans un fichier csv
    if os.path.exists(CSV_FILEPATH):
        new_df.to_csv(CSV_FILEPATH, mode='a', header=False, index=False)

    else:
        new_df.to_csv(CSV_FILEPATH, index=False)
