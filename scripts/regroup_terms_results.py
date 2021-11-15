"""
Ce script permet de combiner les résultats du script `find_terms_frequency.py`.
Ce dernier trouve la fréquence des termes par document, et les ajoute à un fichier csv.
Ce script, `regroup_terms_results.py`, combine les résultats pour tous les documents
pour obtenir les résultats pour le corpus.
"""
import pandas

df = pandas.read_csv('../data/terms.csv')

new_df = pandas.DataFrame(
    columns=['term', 'totalRawFreq', 'relativeFreqAvg', 'zscoreAvg', 'zscoreRatioAvg', 'tfidfAvg', 'totalTermsCount']
)
terms_without_duplicates = ()

for term in df['term'].unique():
    # On ignore les termes qui ne sont que des chiffres.
    if not term.isalpha():
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


new_df.to_csv('./data/corpus-terms.csv', index=False)

