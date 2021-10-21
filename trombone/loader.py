import glob
import os
from collections import Generator
from typing import List, Tuple

from trombone.cache import Cache


def path_loader(path: str, cache: Cache) -> Generator[Tuple[str, str]]:
    """Retourne un générateur de tuple de list : (filepaths, filenames)"""
    file_paths = glob.glob(path)

    for filepath in file_paths:
        filename = os.path.basename(filepath)

        if cache.has_been_processed(filename):
            continue

        yield filepath, filename


def path_loader_batch(path: str, batch_size: int, cache: Cache) -> Generator[Tuple[List[str], List[str]]]:
    """Retourne un générateur de tuple de list : (filepaths, filenames)"""
    file_paths = glob.glob(path)

    batch_filepaths, batch_filenames = [], []
    counter = 0

    for filepath in file_paths:
        filename = os.path.basename(filepath)

        if cache.has_been_processed(filename):
            continue

        counter += 1
        batch_filepaths.append(filepath)
        batch_filenames.append(filename)

        if counter == batch_size:
            yield batch_filepaths, batch_filenames

            batch_filepaths, batch_filenames = [], []
            counter = 0

    yield batch_filepaths, batch_filenames
