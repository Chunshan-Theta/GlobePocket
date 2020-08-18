import json
import unittest

from common import MongoBasicClient, MongoFilters

host="cluster0.enocw.mongodb.net"
db_name="MongoDbToolCommonUnittest"
db_list_name="MongoDbToolCommonUnittestMainList"
class MyTestCase(unittest.TestCase):
    def insert(self):
        with MongoBasicClient(host=host,db_name=db_name,db_list_name=db_list_name) as db_client:
            print(db_client.query(label="unitest"))
            db_client.insert(val={"label": "unitest"})
            print(db_client.query(label="unitest"))

    def query(self):
        with MongoBasicClient(host=host,db_name=db_name,db_list_name=db_list_name) as db_client:
            print(db_client.query(label="unitest"))


    def test_query_in(self):
        with MongoBasicClient(host=host,db_name="fbbot_like_pic",db_list_name="user_like") as db_client:
            print(db_client.query_in(shortcode=["B0yUI-njUwK", "B0u5pqjn9mm", "B0yUD21nh4M"]))

    def test_MongoFilters(self):
        fs = MongoFilters()
        fs.add_filter_in(colume="label1", val=["A","B","C"])\
            .add_filter_in(colume="label2", val=["C","D","E"])\
            .add_filter_equal(colume="label3", val="hi")
        print(fs)

    def test_query_or_MongoFilters(self):
        fs = MongoFilters()
        fs.add_filter_in(colume="label1", val=["A","B","C"])\
            .or_filters(MongoFilters().add_filter_equal(colume="label3", val="hi"))

        print(json.dumps(fs, ensure_ascii=False))

    def test_query_or_MongoFilters2(self):


        print(MongoFilters()
              .add_filter_in(colume="shortcode", val=["B0yUI-njUwK", "B", "C"])
              .or_filters(MongoFilters()
                          .add_filter_equal(colume="label3", val="hi")
                          )
              )
    def test_query_or_MongoFilters3(self):


        print(MongoFilters()
              .add_filter_in(colume="shortcode", val=["B0yUI-njUwK", "B", "C"])
              .or_filters(MongoFilters()
                          .add_filter_equal(colume="label3", val="hi")
                          )
              .or_filters(MongoFilters()
                          .add_filter_regex(colume="shortcode",val="^B0u5.*")
                          )
              )

    def test_query_MongoFilters(self):
        fs = MongoFilters()
        fs.add_filter_in(colume="shortcode", val=["B0yUI-njUwK","B","C"])\
            .add_filter_in(colume="label2", val=["C","D","E"])\
            .add_filter_equal(colume="label3", val="hi")
        with MongoBasicClient(host=host, db_name="fbbot_like_pic",
                              db_list_name="user_like") as db_client:
            print(db_client.query_by_filters(filters=fs))

    def test_query_MongoFilters_or(self):

        fs = MongoFilters()
        fs.add_filter_in(colume="shortcode", val=["B0yUI-njUwK","B","C"])\
            .or_filters(MongoFilters().add_filter_equal(colume="label3", val="hi"))
        with MongoBasicClient(host=host, db_name="fbbot_like_pic",
                              db_list_name="user_like") as db_client:
            print(db_client.query_by_filters(filters=fs))

    def test_query_MongoFilters_or(self):

        fs = MongoFilters()
        fs.add_filter_in(colume="shortcode", val=["B0yUI-njUwK","B","C"])\
            .or_filters(MongoFilters().add_filter_equal(colume="label3", val="hi"))
        with MongoBasicClient(host=host, db_name="fbbot_like_pic",
                              db_list_name="user_like") as db_client:
            result = db_client.query_by_filters(filters=MongoFilters()
                                                .add_filter_in(colume="shortcode", val=["B0yUI-njUwK","B","C"])
                                                .or_filters(MongoFilters()
                                                            .add_filter_equal(colume="label3", val="hi")
                                                            )
                                                )
        print(result)

    def test_query_MongoFilters_test(self):

        fs = MongoFilters()
        fs.add_filter_in(colume="shortcode", val=["B0yUI-njUwK","B","C"])\
            .or_filters(MongoFilters().add_filter_equal(colume="label3", val="hi"))
        with MongoBasicClient(host=host, db_name="fbbot_like_pic",
                              db_list_name="user_like") as db_client:
            result = db_client.query_by_filters(filters=MongoFilters()
                                                  .add_filter_in(colume="shortcode", val=["B0yUI-njUwK", "B", "C"])
                                                  .or_filters(MongoFilters()
                                                              .add_filter_equal(colume="label3", val="hi")
                                                              )
                                                  .or_filters(MongoFilters()
                                                              .add_filter_regex(colume="shortcode",val="^B0u5.*")
                                                              )

                                                )
        print(result)


if __name__ == '__main__':
    unittest.main()