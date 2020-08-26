import json
import unittest
import uuid

from MongoDbTool.common import MongoBasicClient, MongoFilters
from util.travel_tool import TravelUnit, new_travel_unit, add_unit_travel_units


class MyTestCase(unittest.TestCase):

    def test_unit(self):
        tu = TravelUnit(owner="test owner", title="title")
        tu.new_unit(shortcode="wwoewe")
        print(tu)
        tu2 = TravelUnit.from_dict(dict(tu))
        print(tu2)

    def test_something_insert(self):
        with MongoBasicClient(host="cluster0.enocw.mongodb.net", db_name="travelHunt", db_list_name="unit") as db_client:
            print(db_client.query())
            tu = TravelUnit(owner="test owner", title="title")
            tu.new_unit(shortcode="wwoewe")
            db_client.insert(val=tu)
            print(db_client.query())

    def test_new_travel(self):
        tu = TravelUnit(owner="test owner", title="title")
        tu.new_unit(shortcode=str(uuid.uuid4()))
        new_travel_unit(tu=tu)

    def test_updated_travel(self):
        add_unit_travel_units("0bcd8a51-550f-4c76-a25e-9a182a985212", str(uuid.uuid4()))



if __name__ == '__main__':
    unittest.main()
