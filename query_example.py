from fb_message_bot.fb_helper import FbHelperBot
from fb_message_bot.fb_quickreply import FbQuickReplyElement, FbQuickReply
from google_helper import get_place_by_text, get_weather,translate
from handler.fb_collection import make_attachment_generic
from sessionscript.manger import SwitchPlan,Stage,RunResult,Plan,SwitchRePattenPlan
from util.ins_explore import export_spot
from util.message import string_unknown_default, re_search_from_ins, string_search_from_ins, string_query_default, \
    string_query_get_date, string_query_location, \
    string_query_get_location, string_query_order_completed, string_not_found_location, string_forcast, string_premote_day
from util.score import default_board
import datetime
import re

from util.search_pic import pic, pic_set_obj

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

class StageQueryInsPostCollention(Stage):
    def run(self,text,sender_id) -> RunResult:


        if text == 'yes':
            location = orders[sender_id]["location"]
            return RunResult(success=True, label="RepeatText", body={
                "bot_actions": [
                    ("QINS", location)
                ]
            })
        else:

            return RunResult(success=True, label="RepeatText", body={
                "bot_actions": [
                    ("MSG", "thanks")
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
            place_types = place['types']
            place_geo_lat = place['geometry']['location']['lat']
            place_geo_lng = place['geometry']['location']['lng']
            orders[sender_id]["location"] = place_name
            orders[sender_id]["location_geo"] = (place_geo_lat,place_geo_lng)
            # 完成訂單
            orders[sender_id]["status"] = "completed"

            return RunResult(success=True, label="StageQueryLocation", body={
                "bot_actions": [
                    ("MSG", string_query_get_location.msg().format(text=place_name)),
                    ("MSG", string_query_order_completed.msg().format(date=orders[sender_id]["date"],location=orders[sender_id]["location"])),
                    ("CPT", (place_geo_lat,place_geo_lng,place_types,datetime.datetime.strptime(orders[sender_id]["date"],"%y/%m/%d"))),
                    #("FbQuickReply", get_yes_or_no())
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
    query_more_posts = Plan(units=[StageQueryInsPostCollention()])

    #
    switch_plan_handler.add_default_plan(plan=default_plan)
    switch_plan_handler.add_plan(switch_label="NEW_ORDER", plan=new_order_plan)
    switch_plan_handler.add_plan(switch_label="QUERY_DATE", plan=query_date_plan)
    switch_plan_handler.add_plan(switch_label="QUERY_LOCATION", plan=query_location_plan)
    switch_plan_handler.add_plan(switch_label="QUERY_POSTS_INS", plan=query_more_posts)

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
        elif "see_posts" not in orders[sender_id] and False:
            user_stage = "QUERY_POSTS_INS"

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


def weather_forcast_decoder(json_obj:dict,location_types=None) -> (str, int):
    def F2C(F):
        return round(float(F-273.15),2)
    k_label = {'pressure': '氣壓', 'humidity': '濕度', 'wind_speed': '風速', 'wind_deg': '風級數',  'clouds': '雲覆蓋率(%)', 'rain': '降雨量(mm)', 'uvi': '紫外線'}

    respond_str = ""
    content_temp = None
    for k, v in json_obj.items():
        if k == 'weather':
            content_temp = f"天氣簡評: {translate.enzh(v[0]['description'])} \n"
            k_label.update({"description":"天氣簡評"})
        elif k == 'temp':
            respond_str += f"白天溫度(度): {F2C(v['max'])} \n"
            respond_str += f"晚上溫度(度): {F2C(v['min'])} \n"
            k_label.update({"temp": "溫度(度)"})
        elif k == 'pop':
            respond_str += f"降雨機率(%): {v*100} \n"
            k_label.update({"pop": "降雨機率(%)"})
        elif k == 'dew_point':
            respond_str += f"露點(度): {F2C(v)} \n"
            k_label.update({"dew_point": "露點(度)"})

        else:
            if k in k_label:
                respond_str += f"{k_label[k]}: {v} \n"
            else:
                pass#respond_str += f"{k}: {v} \n"
    if content_temp is not None:
        respond_str += content_temp

    json_obj.update({"temp": F2C(json_obj['temp']['eve'])})

    ##
    score_obj = default_board.computer(place_detail=json_obj, cause_detail_option=True)

    ##
    worse = score_obj['worse']
    respond_str+="\n"

    for i in range(int(len(worse)/2)):
        respond_str += f"糟糕項目No.{i+1}『{k_label[worse[i][1]]}』: {worse[i][2]} \n"

    ##
    score = score_obj['score']
    score_detail = score_obj['detail']
    respond_str += f"\n本日評分: {int(score*10)} of 10 \n"

    return translate.zhen(respond_str), int(score*10)


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
                location_types = a[1][2]
                date_lable = a[1][3].strftime("%m/%d")
                if local_mode:
                    detail_weather, _ = weather_forcast_decoder(weather['forecast'][date_lable].copy(), location_types)
                    print(string_forcast.msg().format(date=date_lable, detail=detail_weather))
                    #
                    re_date, re_score = 0,0
                    for k, v in weather['forecast'].items():
                        temp_detail_weather, score = weather_forcast_decoder(v, location_types)
                        if score > re_score:
                            re_score = score
                            re_date = k
                            re_detail = temp_detail_weather
                    print(string_premote_day.msg().format(date=re_date,detail=re_detail))

                else:
                    #
                    detail_weather, _ = weather_forcast_decoder(weather['forecast'][date_lable].copy(), location_types)
                    msg = string_forcast.msg().format(date=date_lable, detail=detail_weather)
                    bot_helper.send_text_message(recipient_id=user_id, message=msg)

                    #
                    re_date, re_score = 0, 0
                    for k, v in weather['forecast'].items():
                        temp_detail_weather, score = weather_forcast_decoder(v, location_types)
                        if score > re_score:
                            re_score = score
                            re_date = k
                            re_detail = temp_detail_weather
                    msg = string_premote_day.msg().format(date=re_date, detail=re_detail)
                    bot_helper.send_text_message(recipient_id=user_id, message=msg)
            """
             elif a[0] == "QINS":
                 location = a[1]
                 print(f"資料處理中...")
                 posts_collection = export_spot(location=location)
                 if local_mode:
                     for k,v in posts_collection.items():
                         temp_pic_list = list()
                         for p in v:
                             temp_pic_list.append(pic(**p))
                         pics = pic_set_obj(temp_pic_list)
                         ag = make_attachment_generic(pics_obj=pics)
                         print(k)
                         print(ag)
                 else:
                     for k,v in posts_collection.items():
                         temp_pic_list = list()
                         for p in v:
                             temp_pic_list.append(pic(**p))
                         pics = pic_set_obj(temp_pic_list)
                         ag = make_attachment_generic(pics_obj=pics,bot=bot_helper)
                         bot_helper.send_text_message(recipient_id=user_id,message=k)
                         bot_helper.send_templete_message(recipient_id=user_id,message_obj=ag)
             """

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


def get_10_day(count=7) -> FbQuickReply:
    date_arr = [FbQuickReplyElement(title=(datetime.datetime.today()+datetime.timedelta(days=i)).strftime("%y/%m/%d"), payload="choices Red") for i in range(0,count)]
    FbQuickReply_date_arr = FbQuickReply(text=string_query_default.msg(), elements=date_arr)
    return FbQuickReply_date_arr

def get_yes_or_no() -> FbQuickReply:
    date_arr = [
        FbQuickReplyElement(title="yes", payload=""),
        FbQuickReplyElement(title="no", payload="")
    ]
    FbQuickReply_date_arr = FbQuickReply(text="see more post?", elements=date_arr)
    return FbQuickReply_date_arr


"""
base_massager_handler(received_text = "hihi")
print("-"*20)
base_massager_handler(received_text = "搜尋：大稻埕")
print("-"*20)
"""
"""
print("-"*20)
base_massager_handler(received_text = "hihi",local_mode=True)
print("-"*20)
base_massager_handler(received_text = "20/09/05",local_mode=True)
print("-"*20)
base_massager_handler(received_text = "龍山寺",local_mode=True)
print("-"*20)
base_massager_handler(received_text = "yes",local_mode=True)
print("-"*20)
base_massager_handler(received_text = "hihi",local_mode=True)
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