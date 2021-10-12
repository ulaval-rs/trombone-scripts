import pytest

from trombone import Trombone

TROMBONE_PATH = './bin/trombone-5.2.1-SNAPSHOT-jar-with-dependencies.jar'


@pytest.fixture
def trombone():
    return Trombone(TROMBONE_PATH)


def test_run_coleman_liau_index(trombone):
    args = {
        'tool': 'corpus.DocumentColemanLiauIndex',
        'file': './tests/data/pdfs/',
    }

    output, error = trombone.run(args)

    assert error == ""
    assert output != ""
