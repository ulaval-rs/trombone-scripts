import os
import shelve
from typing import List, Union


class Cache:

    def __init__(self, cache_path: str):
        self.cache_path = cache_path

        self.cache_shelve_filepath = os.path.join(cache_path, 'cache.db')

    def mark_as_processed(self, filenames: Union[List[str], str]):
        if type(filenames) == list:
            for filepath in filenames:
                self._mark_as_processed(filepath)
        else:
            self._mark_as_processed(filenames)

    def _mark_as_processed(self, filename: str):
        with shelve.open(self.cache_shelve_filepath) as db:
            db[filename] = True

    def has_been_processed(self, filename: str) -> bool:
        with shelve.open(self.cache_shelve_filepath) as db:
            return filename in db.keys()
