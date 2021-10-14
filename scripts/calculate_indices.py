import os
from typing import Dict

import pandas

from trombone import Trombone
from trombone.cache import Cache
from trombone.loader import path_loader

PDFS_PATH = '../data/pdfs'
CSV_FILEPATH = '../data/results.csv'
CACHE_DIRECTORY = '../data/'

TOOL_NAMES_AND_INDEX_NAMES = [
    ('DocumentDaleChallIndex', 'daleChallIndex'),
    ('DocumentColemanLiauIndex', 'colemanLiauIndex'),
    ('DocumentSMOGIndex', 'smogIndex'),
    ('DocumentLIXIndex', 'lixIndex'),
    ('DocumentAutomatedReadabilityIndex', 'automatedReadabilityIndex'),
    ('DocumentFOGIndex', 'fogIndex'),
]

trombone = Trombone('../bin/trombone-5.2.1-SNAPSHOT-jar-with-dependencies.jar')
cache = Cache(CACHE_DIRECTORY)


def make_series_from_dict(data: Dict, name: str) -> pandas.Series:
    return pandas.Series(
        data=data[name],
        index=data[name].keys(),
        name=name,
    )


for filepaths in path_loader('../tests/data/pdfs/*.pdf', batch_size=50):
    filepaths = list(filter(cache.has_not_been_processed, filepaths))
    if not filepaths:
        continue

    first_time_in_loop = True
    series = []

    for tool, index_name in TOOL_NAMES_AND_INDEX_NAMES:
        key_values = [
            ('tool', f'corpus.{tool}'),
            # ('storage', 'file'),  # Stock les textes dans des fichiers en cache plutôt que d'utiliser la mémoire vive
        ]
        # Ajout des fichiers à analyser
        key_values += [('file', filepath) for filepath in filepaths]

        output, error = trombone.run(key_values)
        output = trombone.serialize_output(output)

        output = {key.lower(): value for key, value in output.items()}
        index = list(output[tool.lower()].keys())[0]
        results = output[tool.lower()][index]

        # Setup les dictionnaires qui accueilleront les
        ####################################################
        data = {}

        if tool == 'DocumentDaleChallIndex':
            difficult_words_data = {
                'easyWordsCount': {},
                'difficultWordsCount': {},
            }

        if first_time_in_loop:
            common_data = {
                'lettersCount': {},
                'wordsCount': {},
                'sentencesCount': {},
                'wordsWithMoreThanSixLettersCount': {},
                'wordsWithMoreThanTwoSyllablesCount': {},
            }

        # Boucle sur tous les résultats des documents de la batch et pour la mesure/indice calculé
        ####################################################
        for i, result in enumerate(results):
            data[result['docId']] = result[index_name]

            # Lorsque que le test de Dale Chall est fait, on veut garder d'autres statistiques (montrées ci-dessous)
            if tool == 'DocumentDaleChallIndex':
                difficult_words_data['difficultWordsCount'][result['docId']] = result['difficultWordsCount']
                difficult_words_data['easyWordsCount'][result['docId']] = result['easyWordsCount']

            # La première fois qu'un indice est calculé pour une batch de documents, les statistiques du texte sont préservées
            if first_time_in_loop:
                common_data['lettersCount'][result['docId']] = result['text']['lettersCount']
                common_data['wordsCount'][result['docId']] = result['text']['wordsCount']
                common_data['sentencesCount'][result['docId']] = result['text']['sentencesCount']
                common_data['wordsWithMoreThanSixLettersCount'][result['docId']] = result['text']['wordsWithMoreThanSixLettersCount']
                common_data['wordsWithMoreThanTwoSyllablesCount'][result['docId']] = result['text']['wordsWithMoreThanTwoSyllablesCount']

        # Transformation des statistiques du text en un séries, qui pourra ensuite être écrite dans un fichier csv
        if first_time_in_loop:
            series += [
                make_series_from_dict(common_data, name='lettersCount'),
                make_series_from_dict(common_data, name='wordsCount'),
                make_series_from_dict(common_data, name='sentencesCount'),
                make_series_from_dict(common_data, name='wordsWithMoreThanSixLettersCount'),
                make_series_from_dict(common_data, name='wordsWithMoreThanTwoSyllablesCount'),
            ]

            first_time_in_loop = False

        # Ajout des statistiques de Dale Chall
        if tool == 'DocumentDaleChallIndex':
            series += [
                make_series_from_dict(difficult_words_data, name='difficultWordsCount'),
                make_series_from_dict(difficult_words_data, name='easyWordsCount'),
            ]

        # Ajout des résultats de l'indice calculé
        series.append(pandas.Series(data=data, index=data.keys(), name=index_name))

    df = pandas.concat(series, axis=1)

    # Écriture dans un fichier csv
    if os.path.exists(CSV_FILEPATH):
        df.to_csv(CSV_FILEPATH, mode='a', header=False)

    else:
        df.to_csv(CSV_FILEPATH)

    cache.mark_as_processed(filepaths)
