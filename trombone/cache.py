import os
import shelve
from typing import List, Union


class Cache:

    def __init__(self, cache_path: str):
        self.cache_path = cache_path

        self.cache_shelve_filepath = os.path.join(cache_path, 'cache.db')

    def mark_as_processed(self, filepaths: Union[List[str], str]):
        if type(filepaths) == list:
            for filepath in filepaths:
                self._mark_as_processed(filepath)
        else:
            self._mark_as_processed(filepaths)

    def _mark_as_processed(self, filepath: str):
        with shelve.open(self.cache_shelve_filepath) as db:
            db[filepath] = True

    def has_not_been_processed(self, filepath: str) -> bool:
        with shelve.open(self.cache_shelve_filepath) as db:
            return filepath not in db.keys()
