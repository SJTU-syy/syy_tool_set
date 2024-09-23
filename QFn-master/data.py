# coding:utf-8
import csv
import os
import sqlite3
import json
import __builtin__

root = os.path.dirname(__file__)

_format = u"""
WindowData:
    application: {windowData.application}
    type: {windowData.type}
    group: {windowData.group}
    name: {windowData.name}
    icon: {windowData.icon}
    functions: {windowData.functions}
"""


class WindowData(object):
    __slots__ = ("application", "group", "name", "functions", "type", "icon", "label")

    @classmethod
    def load(cls, path=root+"/configs/windows.csv"):
        with open(path, "rb") as read:
            for dictData in csv.DictReader(read):
                dictData["functions"] = [fun for fun in dictData["functions"].split("\n") if fun]
                if not dictData["icon"]:
                    dictData["icon"] = "lush.jpg"
                yield cls(dictData)

    def __init__(self, data):
        self.application = data.get("application")
        self.group = data.get("group")
        self.name = data.get("name")
        self.functions = data.get("functions")
        self.type = data.get("type")
        self.icon = data.get("icon")
        self.label = data.get("label")

    def __str__(self):
        return _format.format(windowData=self).encode("utf-8")


class Argument(object):

    def __getitem__(self, item):
        if not os.path.isfile(os.path.expanduser("~")+"/QFn.db"):
            connect = sqlite3.connect(os.path.expanduser("~")+"/QFn.db")
            cursor = connect.cursor()
            cursor.execute("create table argument (function ntext primary key,argument ntext);")
            connect.commit()
            cursor.close()
            connect.close()
        connect = sqlite3.connect(os.path.expanduser("~")+"/QFn.db")
        cursor = connect.cursor()
        try:
            cursor.execute("select argument from argument where function is '%s'" % item)
        except sqlite3.OperationalError:
            return {}
        value = cursor.fetchone()
        cursor.close()
        connect.close()
        if isinstance(value, tuple):
            return json.loads(value[0])
        return {}

    def __setitem__(self, key, value):
        value = json.dumps(value)
        if not os.path.isfile(os.path.expanduser("~")+"/QFn.db"):
            connect = sqlite3.connect(os.path.expanduser("~")+"/QFn.db")
            cursor = connect.cursor()
            cursor.execute("create table argument (function ntext primary key,argument ntext);")
            connect.commit()
            cursor.close()
            connect.close()
        connect = sqlite3.connect(os.path.expanduser("~")+"/QFn.db")
        cursor = connect.cursor()
        cursor.execute("delete from argument where function='%s';" % key)
        connect.commit()
        cursor.execute("insert into argument values('%s', '%s')" % (key, value))
        connect.commit()
        cursor.close()
        connect.close()


class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]


class Enum(object):

    def __init__(self, *items):
        self.data = AttributeDict()
        self.data.index = 0
        self.data.item = items[0]
        self.data.items_tuple = items

    def __int__(self):
        return self.data.index

    def __float__(self):
        return float(self.data.index)

    def __str__(self):
        return self.data.item

    def __getitem__(self, item):
        if isinstance(item, int):
            result = enum(*self.data.items_tuple)
            result.data.index = item
            result.data.item = self.data.items_tuple[item]
            return result
        else:
            return getattr(self, item)

    def __getattr__(self, item):
        result = enum(*self.data.items_tuple)
        result.data.item = item
        result.data.index = self.data.items_tuple.index(item)
        return result

    def __cmp__(self, other):
        if isinstance(other, (float, int)) :
            return cmp(int(self), other)
        elif isinstance(other, (str, unicode)):
            return cmp(str(self), other)
        elif isinstance(other, Enum):
            return cmp(str(self), other)
        elif hasattr(other, "__int__") or hasattr(other, "__float__"):
            return cmp(int(self), int(other))
        return cmp(str(self), other)

    def __repr__(self):
        return 'enum({items})'.format(items=str(self.data.items_tuple)[1:-2])

enum = Enum
argument = Argument()
__builtin__.enum = Enum
