import pandas

from trombone import Trombone

PDFS_PATH = '../tests/data/pdfs'

trombone = Trombone('../bin/trombone-5.2.1-SNAPSHOT-jar-with-dependencies.jar')

tool_names_and_index_names = [
    ('DocumentDaleChallIndex', 'daleChallIndex'),
    ('DocumentColemanLiauIndex', 'colemanLiauIndex'),
    ('DocumentSMOGIndex', 'smogIndex'),
    ('DocumentLIXIndex', 'lixIndex'),
    ('DocumentAutomatedReadabilityIndex', 'automatedReadabilityIndex'),
    ('DocumentFOGIndex', 'fogIndex'),
]

series = []

first_time_in_loop = True

for tool, index_name in tool_names_and_index_names:
    output, error = trombone.run({
        'tool': f'corpus.{tool}',
        'storage': 'file',  # Stocke les textes déjà parsés dans des fichiers en cache plutôt que d'utiliser la mémoire
        'file': PDFS_PATH,
    })
    output = trombone.serialize_output(output)

    output = {key.lower(): value for key, value in output.items()}
    index = list(output[tool.lower()].keys())[0]
    results = output[tool.lower()][index]

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

    for i, result in enumerate(results):
        data[result['docIndex']] = result[index_name]

        if tool == 'DocumentDaleChallIndex':
            difficult_words_data['difficultWordsCount'][result['docIndex']] = result['difficultWordsCount']
            difficult_words_data['easyWordsCount'][result['docIndex']] = result['easyWordsCount']

        if first_time_in_loop:
            common_data['lettersCount'][result['docIndex']] = result['text']['lettersCount']
            common_data['wordsCount'][result['docIndex']] = result['text']['wordsCount']
            common_data['sentencesCount'][result['docIndex']] = result['text']['sentencesCount']
            common_data['wordsWithMoreThanSixLettersCount'][result['docIndex']] = result['text']['wordsWithMoreThanSixLettersCount']
            common_data['wordsWithMoreThanTwoSyllablesCount'][result['docIndex']] = result['text']['wordsWithMoreThanTwoSyllablesCount']

    if first_time_in_loop:
        series.append(pandas.Series(data=common_data['lettersCount'],
                                    index=common_data['lettersCount'].keys(),
                                    name='lettersCount'))
        series.append(pandas.Series(data=common_data['wordsCount'],
                                    index=common_data['wordsCount'].keys(),
                                    name='wordsCount'))
        series.append(pandas.Series(data=common_data['sentencesCount'],
                                    index=common_data['sentencesCount'].keys(),
                                    name='sentencesCount'))
        series.append(pandas.Series(data=common_data['wordsWithMoreThanSixLettersCount'],
                                    index=common_data['wordsWithMoreThanSixLettersCount'].keys(),
                                    name='wordsWithMoreThanSixLettersCount'))
        series.append(pandas.Series(data=common_data['wordsWithMoreThanTwoSyllablesCount'],
                                    index=common_data['wordsWithMoreThanTwoSyllablesCount'].keys(),
                                    name='wordsWithMoreThanTwoSyllablesCount'))

        first_time_in_loop = False

    if tool == 'DocumentDaleChallIndex':
        series.append(pandas.Series(data=difficult_words_data['difficultWordsCount'],
                                    index=difficult_words_data['difficultWordsCount'].keys(),
                                    name='difficultWordsCount'))
        series.append(pandas.Series(data=difficult_words_data['easyWordsCount'],
                                    index=difficult_words_data['easyWordsCount'].keys(),
                                    name='easyWordsCount'))

    series.append(pandas.Series(data=data, index=data.keys(), name=index_name))

df = pandas.concat(series, axis=1)
df.to_csv('../data/results.csv')
print(df)
