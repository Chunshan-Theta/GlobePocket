from fb_message_bot.fb_helper import FbHelperBot
from google_helper import get_place_by_text
from sessionscript.manger import SwitchPlan,Stage,RunResult,Plan,SwitchRePattenPlan
from util.message import string_unknown_default,re_search_from_ins,string_search_from_ins,string_query_default,string_query_get_date,string_query_location,\
    string_query_get_location,string_query_order_completed,string_not_found_location



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
                ("MSG", string_query_default.msg())
            ]
        })

class StageQueryDate(Stage):
    def run(self,text,sender_id) -> RunResult:
        #print(text,sender_id)
        if text not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return RunResult(success=True, label="RepeatText", body={
                "bot_actions": [
                    ("MSG", string_query_default.msg())
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
            place_name = places["candidates"][0]['name']
            orders[sender_id]["location"] = place_name

            # 完成搜集時間與地點
            orders[sender_id]["status"] = "completed"
            return RunResult(success=True, label="StageQueryLocation", body={
                "bot_actions": [
                    ("MSG", string_query_get_location.msg().format(text=place_name)),
                    ("MSG", string_query_order_completed.msg().format(date=orders[sender_id]["date"],location=orders[sender_id]["location"]))
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


def base_massager_handler(received_text = "hihi",user_id="123456788", bot_helper: FbHelperBot=None):

    def bot_actions(res: RunResult):
        for i in res.json()['body']['data']:
            return i['body']['bot_actions']

    def bot_action_decode(actions: list):
        for a in actions:
            if a[0] == 'MSG':
                #print(f"BOT: {a[1]}")
                bot_helper.send_text_message(message=a[1],recipient_id=user_id)

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

"""
base_massager_handler(received_text = "hihi")
print("-"*20)
base_massager_handler(received_text = "搜尋：大稻埕")
print("-"*20)
base_massager_handler(received_text = "hihi")
print("-"*20)
base_massager_handler(received_text = "1")
print("-"*20)
base_massager_handler(received_text = "板橋車站")
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