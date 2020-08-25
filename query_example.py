from sessionscript.manger import SwitchPlan,Stage,RunResult,Plan,SwitchRePattenPlan
from util.message import string_unknown_default,re_search_from_ins,string_search_from_ins,string_query_default,string_query_get_date,string_query_location,string_query_get_location,string_query_order_completed

class chatbot_default(Stage):
    def run(self,text,sender_id) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": string_unknown_default.msg().format(text=text)
        })

class StageSearchFromIns(Stage):
    def run(self,text,sender_id) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": string_search_from_ins.msg().format(text=text)
        })


class StageQueryNewOrder(Stage):
    def run(self,text,sender_id) -> RunResult:
        # new client
        if sender_id not in orders:
            orders[sender_id] = {}
        return RunResult(success=True, label="StageNewQuery", body={
            "txt": string_query_default.msg()
        })

class StageQueryDate(Stage):
    def run(self,text,sender_id) -> RunResult:
        #print(text,sender_id)
        if text not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return RunResult(success=True, label="RepeatText", body={
                "txt": string_query_default.msg()
            })
        else:
            # 蒐集到時間
            orders[sender_id]["date"] = text
            print(string_query_get_date.msg().format(text=text))
            return RunResult(success=True, label="StageQueryDate", body={
                "txt": string_query_location.msg()
            })
class StageQueryLocation(Stage):
    def run(self,text,sender_id) -> RunResult:
        # 蒐集到地點
        orders[sender_id]["location"] = text
        print("BOT: ",string_query_get_location.msg().format(text=text))

        # 完成搜集時間與地點
        return RunResult(success=True, label="StageQueryLocation", body={
            "txt": string_query_order_completed.msg().format(date=orders[sender_id]["date"],
                                                             location=orders[sender_id]["location"])
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
        if sender_id  not in orders:
            user_stage = "NEW_ORDER"
        elif "date" not in orders[sender_id]:
            user_stage = "QUERY_DATE"
        elif "location" not in orders[sender_id]:
            user_stage = "QUERY_LOCATION"

        if user_stage is not None:
            #print("\t",user_stage,text,sender_id)
            res = self.switch_plan_handler.switch_and_run_finish(switch_label=user_stage, text=text,sender_id=sender_id)
            res = res.json()['body']['data'][0]['body']['txt']
            return RunResult(success=True, label="RepeatText", body={
                "txt": res
            })


        else:
            return RunResult(success=True, label="RepeatText", body={
                "txt": string_query_default.msg()
            })

def base_massager_handler(received_text = "hihi",user_id="123456788"):
    print(f"client:{received_text}")
    def bot_respond(res: RunResult):
        for i in res.json()['body']['data']:
            print("BOT: ", i['body']['txt'])

    switch_plan_handler = SwitchRePattenPlan()
    default_plan = Plan(units=[StageQueryDefaultSwitch()])
    base_responds_plan = Plan(units=[StageSearchFromIns()])

    #
    switch_plan_handler.add_default_plan(plan=default_plan)
    switch_plan_handler.add_plan(re_patten=re_search_from_ins.msg(), plan=base_responds_plan)

    #
    bot_respond(switch_plan_handler.switch_and_run_finish(switch_label=received_text, text=received_text,sender_id=user_id))

orders = {}
base_massager_handler(received_text = "hihi")
print("-"*20)
base_massager_handler(received_text = "搜尋：大稻埕")
print("-"*20)
base_massager_handler(received_text = "hihi")
print("-"*20)
base_massager_handler(received_text = "1")
print("-"*20)
base_massager_handler(received_text = "板橋車站")

