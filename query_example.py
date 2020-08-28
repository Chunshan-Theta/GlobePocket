from fb_message_bot.fb_helper import FbHelperBot
from fb_message_bot.fb_quickreply import FbQuickReplyElement, FbQuickReply
from google_helper import get_place_by_text, get_weather
from sessionscript.manger import SwitchPlan,Stage,RunResult,Plan,SwitchRePattenPlan
from util.message import string_unknown_default, re_search_from_ins, string_search_from_ins, string_query_default, \
    string_query_get_date, string_query_location, \
    string_query_get_location, string_query_order_completed, string_not_found_location, string_forcast
import datetime
import re

orders = {}
class chatbot_default(Stage):
    def run(self,text,sender_id) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "bot_actions": [
                ("MSG", string_unknown_default.msg().format(text=text))
            ]
        })

class StageSearchFromIns(Stage):
    def run(self,text,sender_id) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "bot_actions": [
                ("MSG", string_search_from_ins.msg().format(text=text))
            ]
        })


class StageQueryNewOrder(Stage):
    def run(self,text,sender_id) -> RunResult:

        # new client
        if sender_id not in orders :
            orders[sender_id] = {"status":"running"}
        elif orders[sender_id]["status"] == "completed":
            orders[sender_id] = {"status": "running"}
        return RunResult(success=True, label="StageNewQuery", body={
            "bot_actions": [
                ("FbQuickReply", get_10_day())
            ]
        })

class StageQueryDate(Stage):
    def run(self,text,sender_id) -> RunResult:
        #print(text,sender_id)
        if re.match(r"\d{2}\/[0,1]{1}\d{1}\/[0,1,2,3]{1}\d{1}",text,re.MULTILINE) is None:
            return RunResult(success=True, label="RepeatText", body={
                "bot_actions": [
                    ("FbQuickReply", get_10_day())
                ]
            })
        else:
            # 蒐集到時間
            orders[sender_id]["date"] = text
            print(string_query_get_date.msg().format(text=text))
            return RunResult(success=True, label="StageQueryDate", body={
                "bot_actions": [
                    ("MSG", string_query_location.msg())
                ]
            })
class StageQueryLocation(Stage):
    def run(self,text,sender_id) -> RunResult:

        places = get_place_by_text(text=text)
        if len(places["candidates"]) >= 1:
            # 蒐集到地點
            place = places["candidates"][0]
            place_name = place['name']
            place_geo_lat = place['geometry']['location']['lat']
            place_geo_lng = place['geometry']['location']['lng']
            orders[sender_id]["location"] = place_name
            orders[sender_id]["location_geo"] = (place_geo_lat,place_geo_lng)

            # 完成搜集時間與地點
            orders[sender_id]["status"] = "completed"
            return RunResult(success=True, label="StageQueryLocation", body={
                "bot_actions": [
                    ("MSG", string_query_get_location.msg().format(text=place_name)),
                    ("MSG", string_query_order_completed.msg().format(date=orders[sender_id]["date"],location=orders[sender_id]["location"])),
                    ("CPT", (place_geo_lat,place_geo_lng,datetime.datetime.strptime(orders[sender_id]["date"],"%y/%m/%d")))
                ]
            })
        else:
            return RunResult(success=True, label="StageQueryDate", body={
                "bot_actions": [
                    ("MSG", string_not_found_location.msg().format(text=text)),
                    ("MSG", string_query_location.msg())
                ]
            })



class StageQueryDefaultSwitch(Stage):
    #
    switch_plan_handler = SwitchPlan()
    default_plan = Plan(units=[StageQueryNewOrder()])
    new_order_plan = Plan(units=[StageQueryNewOrder()])
    query_date_plan = Plan(units=[StageQueryDate()])
    query_location_plan = Plan(units=[StageQueryLocation()])

    #
    switch_plan_handler.add_default_plan(plan=default_plan)
    switch_plan_handler.add_plan(switch_label="NEW_ORDER", plan=new_order_plan)
    switch_plan_handler.add_plan(switch_label="QUERY_DATE", plan=query_date_plan)
    switch_plan_handler.add_plan(switch_label="QUERY_LOCATION", plan=query_location_plan)

    def run(self,text,sender_id) -> RunResult:
        user_stage = None
        if sender_id not in orders:
            user_stage = "NEW_ORDER"
        elif orders[sender_id]["status"] == "completed":
            user_stage = "NEW_ORDER"
        elif "date" not in orders[sender_id]:
            user_stage = "QUERY_DATE"
        elif "location" not in orders[sender_id]:
            user_stage = "QUERY_LOCATION"

        if user_stage is not None:
            res = self.switch_plan_handler.switch_and_run_finish(switch_label=user_stage, text=text,sender_id=sender_id)
            res_bot_actions = res.json()['body']['data'][0]['body']['bot_actions']
            return RunResult(success=True, label="StageQueryDefaultSwitch", body={
                "bot_actions": res_bot_actions
            })

        else:
            return RunResult(success=True, label="StageQueryDefaultSwitch_unknown_situation", body={
                "bot_actions": [
                    ("MSG", f"{string_query_default.msg()},{orders[sender_id]}")
                ]

            })


def base_massager_handler(received_text = "hihi",user_id="123456788", bot_helper: FbHelperBot=None,local_mode=False):

    def bot_actions(res: RunResult):
        for i in res.json()['body']['data']:
            return i['body']['bot_actions']

    def bot_action_decode(actions: list):
        for a in actions:
            if a[0] == "MSG":
                if local_mode:
                    print(f"BOT: {a[1]}")
                else:
                    bot_helper.send_text_message(message=a[1],recipient_id=user_id)
            elif a[0] == "FbQuickReply":
                if local_mode:
                    print(f"BOT: {a[1]}")
                else:
                    bot_helper.send_quickreplay_message(recipient_id=user_id,message_obj=a[1])
            elif a[0] == "CPT":
                weather = get_weather(a[1][0], a[1][1])
                week = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
                date = a[1][2].strftime("%m/%d")
                date_day = a[1][2].strftime("%d")
                date_lable = f"{week[a[1][2].weekday()]} {date_day}"
                if local_mode:
                    if 'Day' in weather['forecast'][date_lable]:
                        detail_weather = str(weather['forecast'][date_lable]['Day'])
                        print(string_forcast.msg().format(date=date,time="白天",detail=detail_weather))
                    if 'Night' in weather['forecast'][date_lable]:
                        detail_weather = str(weather['forecast'][date_lable]['Night'])
                        print(string_forcast.msg().format(date=date, time="晚上", detail=detail_weather))
                else:
                    if 'Day' in weather['forecast'][date_lable]:
                        detail_weather = str(weather['forecast'][date_lable]['Day'])
                        msg = string_forcast.msg().format(date=date, time="白天", detail=detail_weather)
                        bot_helper.send_text_message(recipient_id=user_id, message=msg)
                    if 'Night' in weather['forecast'][date_lable]:
                        detail_weather = str(weather['forecast'][date_lable]['Night'])
                        msg = string_forcast.msg().format(date=date, time="晚上", detail=detail_weather)
                        bot_helper.send_text_message(recipient_id=user_id, message=msg)

    #
    print(f"Client: {received_text}")
    switch_plan_handler = SwitchRePattenPlan()
    default_plan = Plan(units=[StageQueryDefaultSwitch()])
    base_responds_plan = Plan(units=[StageSearchFromIns()])

    #
    switch_plan_handler.add_default_plan(plan=default_plan)
    switch_plan_handler.add_plan(re_patten=re_search_from_ins.msg(), plan=base_responds_plan)

    #
    bot_actions = bot_actions(switch_plan_handler.switch_and_run_finish(switch_label=received_text, text=received_text,sender_id=user_id))
    bot_action_decode(bot_actions)


def get_10_day() -> FbQuickReply:
    date_arr = [FbQuickReplyElement(title=(datetime.datetime.today()+datetime.timedelta(days=i)).strftime("%y/%m/%d"), payload="choices Red") for i in range(0,10)]
    FbQuickReply_date_arr = FbQuickReply(text=string_query_default.msg(), elements=date_arr)
    return FbQuickReply_date_arr

"""
base_massager_handler(received_text = "hihi")
print("-"*20)
base_massager_handler(received_text = "搜尋：大稻埕")
print("-"*20)
"""
"""
base_massager_handler(received_text = "hihi")
print("-"*20)
base_massager_handler(received_text = "20/08/29")
print("-"*20)
base_massager_handler(received_text = "板橋車站")
"""
"""
print("-"*20)
base_massager_handler(received_text = "hihi")
print("-"*20)
base_massager_handler(received_text = "2")
print("-"*20)
base_massager_handler(received_text = "台北101")
print("-"*20)
base_massager_handler(received_text = "hihi")
print("-"*20)
base_massager_handler(received_text = "3")
print("-"*20)
base_massager_handler(received_text = "qweksalhfoiqweqw")
print("-"*20)
base_massager_handler(received_text = "新北市都會公園")
print("-"*20)
base_massager_handler(received_text = "hi",user_id="user1")
print("-"*20)
base_massager_handler(received_text = "hi",user_id="user2")
print("-"*20)
base_massager_handler(received_text = "1",user_id="user1")
print("-"*20)
base_massager_handler(received_text = "清境農場",user_id="user1")
print("-"*20)
base_massager_handler(received_text = "2",user_id="user2")
print("-"*20)
base_massager_handler(received_text = "武陵",user_id="user2")
"""