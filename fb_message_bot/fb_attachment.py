from fb_message_bot.fb_button import FbButtom,Demo_btn_set


class AttachmentButton(dict):
    def __init__(self,text,buttons:[FbButtom]):
        super().__init__()
        assert len(buttons) <= 3, "buttons max limit: 3"
        self.update({
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons":buttons
                    }
                }
            })


class AttachmentGenericPayloadElements(dict):
    def __init__(self, title, subtitle, image_url, default_url, buttons:[FbButtom], fallback_url=None):
        super().__init__()
        assert len(buttons) <= 3, "buttons max limit: 3"
        fallback_url = fallback_url if fallback_url is not None else default_url
        self.update({
            "title": title,
            "image_url": image_url,
            "subtitle": subtitle,
            "default_action": {
                "type": "web_url",
                "url": default_url,
                "messenger_extensions": "true",
                "webview_height_ratio": "tall",
                "fallback_url": fallback_url
            },
            "buttons": buttons
        })




class AttachmentGeneric(dict):
    def __init__(self,elements:[AttachmentGenericPayloadElements],skip=0):
        #assert len(elements) <= 10, "AttachmentGeneric elements max limit: 10"
        super().__init__()
        self.update({
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements[skip:skip+9]
                    }
                }
            })
default_url = "https://www.silkrode.com.tw/"
image_url = "https://instagram.ftpe8-2.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/s640x640/98260439_922980594830667_8922216794545382042_n.jpg?_nc_ht=instagram.ftpe8-2.fna.fbcdn.net&_nc_cat=103&_nc_ohc=Pjc1OkZbkiQAX8kO77a&oh=6fcbb12b0628402f09e4955e46747529&oe=5F31A8ED"
Demo_GenericPayloadElement_set = list()
Element1 = AttachmentGenericPayloadElements(title="工具1", subtitle="最棒的工具1", image_url=image_url, default_url=default_url, buttons=Demo_btn_set)
Element2 = AttachmentGenericPayloadElements(title="工具2", subtitle="最棒的工具2", image_url=image_url, default_url=default_url, buttons=Demo_btn_set)
Demo_GenericPayloadElement_set.append(Element1)
Demo_GenericPayloadElement_set.append(Element2)
Demo_AttachmentGeneric = AttachmentGeneric(elements=Demo_GenericPayloadElement_set)
Demo_AttachmentButton = AttachmentButton(text="What do you want to do next?", buttons=Demo_btn_set)

