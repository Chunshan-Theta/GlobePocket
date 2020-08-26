
class FbButtom(dict):
    def __init__(self):
        super().__init__()
        button_type_list = ["web_url", "postback", "phone_number", "account_link"]
        assert self.__getitem__("type") in button_type_list, "no support button type"


class FbButtomURL(FbButtom):
    def __init__(self, url:str, title:str):

        self.__setitem__("type", "web_url")
        self.__setitem__("url", url)
        self.__setitem__("title", title)
        super().__init__()


class FbButtomPostBack(FbButtom):
    def __init__(self, payload:str, title:str):

        self.__setitem__("type", "postback")
        self.__setitem__("payload", payload)
        self.__setitem__("title", title)
        super().__init__()

Demo_btn_set = list()
Demo_btn_set.append(FbButtomPostBack(payload="clicked", title="我有興趣"))
Demo_btn_set.append(FbButtomURL(url="https://www.silkrode.com.tw/", title="前進網站"))