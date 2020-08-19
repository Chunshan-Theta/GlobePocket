import json
import unittest
from unittest import mock
from common import MongoBasicClient, MongoFilters

host="host_server"
db_name="db_name"
db_list_name="db_list_name"


class MyTestCase(unittest.TestCase):

    @mock.patch('common.MongoBasicClient.init_client', return_value={db_name: {db_list_name:"db_list_name"}})
    @mock.patch('common.MongoBasicClient.__exit__',return_value=None)
    def test_MongoBasicClient_init(self,*agrs):
        ans = {'user': 'pythontest', 'password': 'pythontest', 'host': 'host_server', 'db_name': 'db_name', 'ObjClient': "{'db_name': {'db_list_name': 'db_list_name'}}", 'SelectedDB': "{'db_list_name': 'db_list_name'}", 'SelectedList': 'db_list_name', 'insert': '<bound method MongoBasicClient.insert of <common.MongoBasicClient object at 0x10fc04fd0>>', 'insert_multi': '<bound method MongoBasicClient.insert_multi of <common.MongoBasicClient object at 0x10fc04fd0>>', 'query': '<bound method MongoBasicClient.query of <common.MongoBasicClient object at 0x10fc04fd0>>', 'query_by_filters': '<bound method MongoBasicClient.query_by_filters of <common.MongoBasicClient object at 0x10fc04fd0>>', 'query_in': '<bound method MongoBasicClient.query_in of <common.MongoBasicClient object at 0x10fc04fd0>>', 'update': '<bound method MongoBasicClient.update of <common.MongoBasicClient object at 0x10fc04fd0>>', 'change_user': '<bound method MongoBasicClient.change_user of <common.MongoBasicClient object at 0x10fc04fd0>>', 'select_list': '<bound method MongoBasicClient.select_list of <common.MongoBasicClient object at 0x10fc04fd0>>', 'init_client': "<MagicMock name='init_client' id='4554035472'>"}


        with MongoBasicClient(host=host,db_name=db_name,db_list_name=db_list_name) as db_client:
            obj = db_client.__json__()
            print(obj)
            for k,v in ans.items():
                self.assertEqual(len(v),len(obj[k]))
                self.assertEqual(type(v),type(obj[k]))


    def test_MongoFilters(self):
        fs = MongoFilters()
        fs.add_filter_in(colume="label1", val=["A","B","C"])\
            .add_filter_in(colume="label2", val=["C","D","E"])\
            .add_filter_equal(colume="label3", val="hi")
        ans = {'label1': {'$in': ['A', 'B', 'C']}, 'label2': {'$in': ['C', 'D', 'E']}, 'label3': 'hi'}
        self.assertEqual(fs,ans)

    def test_query_or_MongoFilters(self):
        fs = MongoFilters()
        fs.add_filter_in(colume="label1", val=["A","B","C"])\
            .or_filters(MongoFilters().add_filter_equal(colume="label3", val="hi"))

        ans = {"$or": [{"label1": {"$in": ["A", "B", "C"]}}, {"label3": "hi"}]}
        self.assertEqual(ans,fs)


if __name__ == '__main__':
    unittest.main()
