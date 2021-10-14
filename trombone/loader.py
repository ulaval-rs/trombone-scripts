import glob
from collections import Generator
from typing import List


def path_loader(path: str, batch_size: int) -> Generator[List[str]]:
    file_paths = glob.glob(path)

    batch = []
    counter = 0

    for file_path in file_paths:
        counter += 1
        batch.append(file_path)

        if counter == batch_size:
            yield batch

            batch = []
            counter = 0

    yield batch
