from sessionscript.manger import SwitchPlan,Stage,RunResult,Plan,SwitchRePattenPlan
from util.message import string_unknown_default,re_search_from_ins,string_search_from_ins


class chatbot_default(Stage):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": string_unknown_default.msg().format(text=text)
        })

class StageSearchFromIns(Stage):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": string_search_from_ins.msg().format(text=text)
        })





def base_massager_handler(received_text = "hihi"):
    def bot_respond(res: RunResult):
        for i in res.json()['body']['data']:
            print("BOT: ", i['body']['txt'])

    switch_plan_handler = SwitchRePattenPlan()
    default_plan = Plan(units=[chatbot_default()])
    base_responds_plan = Plan(units=[StageSearchFromIns()])

    #
    switch_plan_handler.add_default_plan(plan=default_plan)
    switch_plan_handler.add_plan(re_patten=re_search_from_ins.msg(), plan=base_responds_plan)

    #
    print('-' * 20)
    bot_respond(switch_plan_handler.switch_and_run_finish(switch_label=received_text, text=received_text))


base_massager_handler(received_text = "hihi")
base_massager_handler(received_text = "搜尋：大稻埕")