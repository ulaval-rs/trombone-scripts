import shelve
from typing import List, Union


class Cache:

    def __init__(self, cache_path: str):
        self.cache_shelve_filepath = cache_path

    def mark_as_processed(self, filenames: Union[List[str], str]):
        if type(filenames) == list:
            for filename in filenames:
                self._mark_as_processed(filename)
        else:
            self._mark_as_processed(filenames)

    def mark_as_failed(self, filenames: Union[List[str], str]):
        if type(filenames) == list:
            for filename in filenames:
                self._mark_as_failed(filename)
        else:
            self._mark_as_failed(filenames)

    def _mark_as_processed(self, filename: str):
        with shelve.open(self.cache_shelve_filepath) as db:
            db[filename] = True

    def _mark_as_failed(self, filename: str):
        with shelve.open(self.cache_shelve_filepath) as db:
            db[filename] = False

    def has_been_processed(self, filename: str) -> bool:
        with shelve.open(self.cache_shelve_filepath) as db:
            if filename in db:
                if db[filename]:
                    return True

            return False
