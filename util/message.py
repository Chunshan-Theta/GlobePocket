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
