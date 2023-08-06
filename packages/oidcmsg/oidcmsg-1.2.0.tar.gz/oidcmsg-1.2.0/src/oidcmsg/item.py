from typing import List
from typing import Optional

from oidcmsg.impexp import ImpExp
from oidcmsg.storage import importer


class ImpExpDict(ImpExp):
    def __init__(self):
        ImpExp.__init__(self)
        self._db = {}

    def set(self, key, value, value_cls):
        self._db[key] = (value, value_cls)

    def __getitem__(self, key):
        value, _ = self._db[key]
        return value

    def get(self, key, default=None):
        try:
            value, _ = self._db[key]
        except KeyError:
            value = default
        return value

    def dump(self, exclude_attributes: Optional[List[str]] = None) -> dict:
        res = {}
        for key, (value, value_cls) in self._db.items():
            res[key] = (value.dump(exclude_attributes=exclude_attributes), value_cls)

        return res

    def load(self, item):
        for key, (value, value_cls) in item.items():
            val = importer(value_cls)().load(value)
            self._db[key] = (val, value_cls)
        return self

    def keys(self):
        return self._db.keys()

    def items(self):
        return {k: v for k, (v, _) in self._db.items()}.items()


class UniDict(ImpExp):
    parameter = {
        "item_class": "",
        "db": {}
    }

    def __init__(self, item_class: Optional[str] = ""):
        ImpExp.__init__(self)
        self.item_class = item_class
        self.db = {}

    def __setitem__(self, key: str, val):
        self.db[key] = val

    def __getitem__(self, key: str):
        return self.db[key]

    def dump(self, exclude_attributes: Optional[List[str]] = None) -> dict:
        res = {
            "item_class": self.item_class,
            "db": {k: v.dump(exclude_attributes=exclude_attributes) for k, v in
                   self.db.items()}
        }
        return res

    def load(self, spec: dict) -> "UniDict":
        _item_class = spec.get("item_class")
        if not _item_class:
            raise ValueError("Missing item_class specification")

        self.item_class = _item_class
        _class = importer(_item_class)
        for attr, item in spec["db"].items():
            self.db[attr] = _class().load(item)

        return self

    def keys(self):
        return self.db.keys()

    def items(self):
        return self.db.items()
