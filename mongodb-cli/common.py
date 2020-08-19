import json

import typing
from bson import json_util
from pymongo import MongoClient
from pymongo.results import InsertOneResult, InsertManyResult
import datetime
from uuid import uuid4


class MongoFilters(dict):
    def __init__(self):
        super().__init__()

    def add_filter(self,colume:str, operation, val):
        if colume not in self.keys():
            self.__setitem__(colume,{})
        tmp_colume:dict = self.__getitem__(colume)
        tmp_colume[operation] = val

    def add_filter_in(self,colume:str, val:list):
        self.add_filter(colume=colume, operation="$in", val=val)
        return self

    def add_filter_greater(self,colume:str, val:list,equal_contain=False):
        if equal_contain:
            self.add_filter(colume=colume, operation="$gte", val=val)
        else:
            self.add_filter(colume=colume, operation="$gt", val=val)
        return self

    def add_filter_lesser(self,colume:str, val:list, equal_contain=False):
        if equal_contain:
            self.add_filter(colume=colume, operation="$lte", val=val)
        else:
            self.add_filter(colume=colume, operation="$lt", val=val)
        return self

    def add_filter_equal(self, colume: str, val: str):
        self.__setitem__(colume,val)
        return self

    def add_filter_not_equal(self,colume:str, val:list):
        self.add_filter(colume=colume, operation="$ne", val=val)
        return self

    def add_filter_regex(self, colume:str, val:str):
        self.add_filter(colume=colume, operation="$regex", val=val)
        return self

    def or_filters(self, filters=None):
        assert filters is None or isinstance(filters, MongoFilters),\
            "filters type need dict or MongoFilters, or keep empty"
        if filters is None:
            self.__setitem__("$or", [dict(self)])
        else:
            if "$or" not in self.keys():
                self.__setitem__("$or", [dict(self), dict(filters)])
            else:
                or_list:list = self.__getitem__("$or")
                or_list.append(dict(filters))

        for key in list(self.keys()).copy():
            if key != "$or":
                self.pop(key, None)
        return self

class MongoBasicClient:
    def __init__(self, host, db_name, db_list_name, user= "pythontest", password= "pythontest"):
        self.user = user
        self.password = password
        self.host = host
        self.db_name = db_name
        self.ObjClient = self.init_client()
        self.SelectedDB = self.ObjClient[db_name]
        self.SelectedList = self.SelectedDB[db_list_name]
        self._date_fmt = "%Y/%m/%d %H:%M:%S"

    def insert(self, val: dict):
        default = {
            "uuid": str(uuid4()),
            "created": datetime.datetime.now().strftime(self._date_fmt),
            "updated": datetime.datetime.now().strftime(self._date_fmt)
        }
        val.update(default)
        insert_result: InsertOneResult = self.SelectedList.insert_one(document=val)
        return insert_result

    def query(self,projection: dict = None,limit: int = 0, **kwargs):

        if projection is None:
            return list(self.SelectedList.find(limit=limit, filter= kwargs))

        else:
            return list(self.SelectedList.find(limit=limit, filter= kwargs, projection=projection))

    def query_by_filters(self, filters: MongoFilters, projection: dict = None):

        if projection is None:
            return list(self.SelectedList.find(filter= filters))

        else:
            return list(self.SelectedList.find(filter= filters, projection=projection))

    def query_in(self, **kwargs):
        return self.query(**{key:{"$in": val} for key, val in kwargs.items()})

    def update(self,filters:dict, **kwargs):
        default = {
            "updated": datetime.datetime.now().strftime(self._date_fmt)
        }
        kwargs.update(default)
        if "uuid" in kwargs:
            kwargs.pop("uuid")
        newvalues = {"$set": kwargs}

        self.SelectedList.update_many(filters, newvalues)

    def delete(self, **kwargs):

        self.SelectedList.delete_many(kwargs)

    ##
    def change_user(self,account,pws):
        if isinstance(self.ObjClient, MongoClient):
            self.ObjClient.close()
        self.user = account
        self.password = pws
        self.ObjClient = self.init_client()

    def select_list(self,name):
        self.SelectedList = self.SelectedDB[name]

    def init_client(self):
        return MongoClient(host=f"mongodb+srv://{self.user}:{self.password}@{self.host}/{self.db_name}?retryWrites=true&w=majority")

    ##
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.ObjClient.close()

    def __str__(self):
        return str(self.__json__())

    def __json__(self):
        return {i: str(self.__getattribute__(i)) for i in self.__dir__() if not i.startswith("_")}


