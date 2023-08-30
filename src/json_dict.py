from contextlib import contextmanager
from functools import wraps
import os
import json
import logging


class JsonDict(dict):

    def __init__(self, *args,json_path=None, logger=None, **kw):
        super(type(self),self).__init__(*args, **kw)
        self._logger = logging.getLogger(__name__) if logger is None else logger
        self.__path = json_path
        self.__save_on_write = 1
        if json_path is not None:
            if os.path.exists(self.__path):
                self.__load_from_file()
            self.__save_on_write = 0

    def __setitem__(self, key, value):
        super(type(self),self).__setitem__(key, value)
        self.__save_to_file()

    def __iter__(self):
        return iter(self.itemlist)

    def get_directory(self):
        return os.path.dirname(self.__path)

    @property
    def item_list(self):
        return super(type(self),self).keys()

    def values(self):
        return [self[key] for key in self]  

    def itervalues(self):
        return (self[key] for key in self)

    def __load_from_file(self):
        with open(self.__path) as log:
            tmp = json.loads(log.read())
        for key,val in tmp.items():
            self[key] = val

    def __save_to_file(self):
        if 0 == self.__save_on_write:
           self._logger.debug(f"{type(self)} save json")
           with open(self.__path, 'w') as log:
               log.write(json.dumps(self, indent=2))

    @contextmanager
    def suspend_writing(self):
        self.__save_on_write += 1
        self._logger.debug(f"{type(self)} suspend writing level {self.__save_on_write}")
        yield
        self.__save_on_write -= 1
        self._logger.debug(f"{type(self)} suspend writing level {self.__save_on_write}")
        self.__save_to_file()

    def bulk_update(self, func):
        @wraps
        def wrapper(*args, **kwargs):
            with self.suspend_writing():
                func(*args,**kwargs)
        return wrapper
