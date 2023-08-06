import logging

from .utils import importer

logger = logging.getLogger(__name__)


class Handler(object):
    """
    An persistent storage handler that offers a standard set of methods and I/O to data.
    """

    def __init__(self, conf_dict):
        pass

    def get(self, key, default=None):
        """
        Find information in the storage based on a key.
        If no information in the storage is bound to the key then the default item is returned.

        :param key:
        :param default:
        :return:
        """
        raise NotImplemented()

    def update(self, ava):
        """

        :param ava: attribute/item assertions:
        """
        raise NotImplemented()

    def delete(self, key, item):
        """
        Remove the item from the key

        :param key:
        :param item:
        :return:
        """
        raise NotImplemented()

    def __getitem__(self, key):
        raise NotImplemented()

    def __setitem__(self, key, item):
        """
        Bind a item to a key.

        :param key:
        :param item:
        """
        raise NotImplemented()

    def __delitem__(self, key):
        """
        Remove the key and any item bound to the key from the storage.

        :param key:
        :return:
        """
        raise NotImplemented()

    def __call__(self):
        """
        Allows the instance to behave like a function.

        :return:
        """
        raise NotImplemented()

    def __repr__(self):
        """
        Returns an object representation of the instance

        :return:
        """
        raise NotImplemented()

    def __len__(self):
        """
        The number of items in the storage.

        :return:
        """
        raise NotImplemented()

    def __contains__(self, key):
        """
        Whether or not the key appears in the storage.

        :param key:
        :return:
        """
        raise NotImplemented()

    def __str__(self):
        """
        Returns an str representation of the instance
        :return:
        """
        return str(self.__repr__())

    def __iter__(self):
        """
        iterate of the keys in the storage.

        :return: An iterator
        """
        raise NotImplemented()

    def sync(self):
        raise NotImplemented()

    def keys(self):
        """
        The set of keys on the storage

        :return:
        """
        raise NotImplemented()

    def items(self):
        """
        A list of key, value tuples.

        :return:
        """
        raise NotImplemented()

    def clear(self):
        """
        Completely resets the database. This means that all information in
        the local cache and on disc will be erased.
        """
        raise NotImplemented()