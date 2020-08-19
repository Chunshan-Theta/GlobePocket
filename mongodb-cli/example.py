import json
import unittest
import random
from common import MongoBasicClient, MongoFilters

host="cluster0.enocw.mongodb.net"
db_name="MongoDbToolCommonUnittest"
db_list_name="MongoDbToolCommonUnittestMainList"


def insert():
    with MongoBasicClient(host=host,db_name=db_name,db_list_name=db_list_name) as db_client:
        print(db_client.query(label="unitest"))
        db_client.insert(val={"label": "unitest"})
        print(db_client.query(label="unitest"))


def query():
    with MongoBasicClient(host=host,db_name=db_name,db_list_name=db_list_name) as db_client:
        print(db_client.query(label="unitest"))


def query_in():
    with MongoBasicClient(host=host,db_name="fbbot_like_pic",db_list_name="user_like") as db_client:
        print(db_client.query_in(shortcode=["B0yUI-njUwK", "B0u5pqjn9mm", "B0yUD21nh4M"]))


def update():
    with MongoBasicClient(host=host,db_name=db_name,db_list_name=db_list_name) as db_client:
        print(db_client.query(uuid="55079a99-81da-45b5-a41f-9a68e07ccfc5"))
        index = random.randint(0, 9)
        db_client.update(filters={"uuid": "55079a99-81da-45b5-a41f-9a68e07ccfc5"}, label=f"unitest-test{index}",label2=f"unitest-test{index}")
        print(db_client.query(uuid="55079a99-81da-45b5-a41f-9a68e07ccfc5"))

def delete():
    with MongoBasicClient(host=host,db_name=db_name,db_list_name=db_list_name) as db_client:
        db_client.delete(label="unitest")

def query_by_mongo_filters():
    fs = MongoFilters()
    fs.add_filter_in(colume="shortcode", val=["B0yUI-njUwK","B","C"])\
        .add_filter_in(colume="label2", val=["C","D","E"])\
        .add_filter_equal(colume="label3", val="hi")

    with MongoBasicClient(host=host, db_name="fbbot_like_pic",db_list_name="user_like") as db_client:
        print(db_client.query_by_filters(filters=fs))


def query_mongo_filters_or():
    fs = MongoFilters()
    fs.add_filter_in(colume="shortcode", val=["B0yUI-njUwK", "B", "C"])
    fs.or_filters(MongoFilters().add_filter_equal(colume="label3", val="hi"))
    with MongoBasicClient(host=host, db_name="fbbot_like_pic",
                          db_list_name="user_like") as db_client:
        print(db_client.query_by_filters(filters=fs))


def query_mongo_filters_or_multi():

    with MongoBasicClient(host=host, db_name="fbbot_like_pic", db_list_name="user_like") as db_client:
        fs = MongoFilters().add_filter_in(colume="shortcode", val=["B0yUI-njUwK","B","C"])
        fs.or_filters(MongoFilters().add_filter_equal(colume="label3", val="hi"))
        fs.or_filters(MongoFilters().add_filter_equal(colume="label3", val="hi2"))

        result = db_client.query_by_filters(filters=fs)

    print(result)

