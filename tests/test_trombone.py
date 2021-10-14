import pytest

from trombone import Trombone

TROMBONE_PATH = './bin/trombone-5.2.1-SNAPSHOT-jar-with-dependencies.jar'


@pytest.fixture
def trombone():
    return Trombone(TROMBONE_PATH)


def test_run_coleman_liau_index(trombone):
    key_values = [
        ('tool', 'corpus.DocumentColemanLiauIndex'),
        ('file', './tests/data/pdfs/'),
        ('file', './tests/data/pdfs/ESPAF_032012_E.pdf'),
    ]

    output, _ = trombone.run(key_values)

    assert output != ""
