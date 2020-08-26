MSG_LANG = "zh"
class Massage(dict):
    def __init__(self,**kwargs):
        super().__init__()
        for k,v in kwargs.items():
            self.__setitem__(k,v)

    def msg(self) -> str:
        return self.get(MSG_LANG)


string_unknown_default = Massage(zh="你好我收到『{text}』但我無法理解",
                                  en="Hello, I can't understand your 『{text}』")

string_search_from_ins = Massage(zh="從Ins中搜尋：『{text}』",
                                  en="search from Ins:『{text}』")

re_search_from_ins = Massage(zh=".?搜尋(:|：).?",
                             en=".?(search|find):.?")

string_query_default = Massage(zh="您好，最近有要安排哪個時間旅遊嗎？")
string_query_location= Massage(zh="請問地點是？")
string_query_get_date = Massage(zh="您好，我已經了解您是要在『{text}』的時候旅遊")
string_query_get_location = Massage(zh="您好，我已經了解您要前往『{text}』")
string_query_order_completed= Massage(zh="您好，我已經了解您要在『{date}』的時候前往『{location}』")
string_not_found_location = Massage(zh="您好，我找不到『{text}』")