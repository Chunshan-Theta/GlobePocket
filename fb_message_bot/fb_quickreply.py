
class FbQuickReplyElement(dict):
    def __init__(self, title: str,payload:str,image_url=None):
        if image_url is not None:
            self.update({
                "content_type": "text",
                "title": title,
                "payload": payload,
                "image_url": image_url
            })
        else:
            self.update({
                "content_type": "text",
                "title": title,
                "payload": payload,
            })


class FbQuickReply(dict):
    def __init__(self,text:str,elements:[FbQuickReplyElement]):
        assert len(elements)<=13,"Max number is 13."
        super().__init__()
        self.update({
            "text": text,
            "quick_replies": elements
        })


Demo_FbQuickReplyElement1 = FbQuickReplyElement(title="Red", payload="choices Red",
                                                image_url="https://www.redbydufry.com/main-slider/main-slider-img1.png")
Demo_FbQuickReplyElement2 = FbQuickReplyElement(title="Green", payload="choices Green",
                                                image_url="https://img.freepik.com/free-vector/attractive-sensual-woman-portrait-wearing-green-hat-earrings-vector-illustration_1284-1950.jpg?size=338&ext=jpg")
Demo_FbQuickReply = FbQuickReply(text="Pick a color:", elements=[Demo_FbQuickReplyElement1, Demo_FbQuickReplyElement2])