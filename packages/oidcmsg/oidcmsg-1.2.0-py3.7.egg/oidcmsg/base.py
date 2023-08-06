import copy
from urllib.parse import quote_plus

from cryptojwt import KeyJar
from cryptojwt.key_jar import init_key_jar
from cryptojwt.utils import importer
from cryptojwt.utils import qualified_name

from oidcmsg.message import Message


def add_issuer(conf, issuer):
    res = {}
    for key, val in conf.items():
        if key == 'abstract_storage_cls':
            res[key] = val
        else:
            _val = copy.copy(val)
            _val['issuer'] = quote_plus(issuer)
            res[key] = _val
    return res


class Base:
    parameter = {}

    def __init__(self):
        pass

    def dump(self):
        info = {}
        for attr, cls in self.parameter.items():
            item = getattr(self, attr, None)
            if item is None:
                continue
            if cls is None:
                info[attr] = item
            elif isinstance(item, Message):
                info[attr] = item.to_dict()
            elif cls == object:
                info[attr] = qualified_name(item)
            else:
                info[attr] = item.dump()

        return info

    def load(self, item):
        for attr, cls in self.parameter.items():
            if attr not in item:
                continue

            if cls is None:
                setattr(self, attr, item[attr])
            elif cls == object:
                setattr(self, attr, importer(item[attr]))
            elif issubclass(cls, Message):
                setattr(self, attr, cls().from_dict(item[attr]))
            else:
                setattr(self, attr, cls().load(item[attr]))
        return self
