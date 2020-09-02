
from fb_message_bot.fb_attachment import AttachmentGeneric, AttachmentGenericPayloadElements
from fb_message_bot.fb_button import FbButtomPostBack,FbButtomURL
from fb_message_bot.fb_quickreply import FbQuickReply, FbQuickReplyElement
from util.ins_explore import ins_get_pic_by_short_code
from util.search_pic import pic_set_obj


def make_attachment_generic(pics_obj:pic_set_obj,bot=None):

    pics = pics_obj.get_pics(count=9)

    #
    pic_sets = list()
    whitelisted_domains = list()

    for p in pics:
        while p['url'].find("https") == -1 or p['media'].find("https") == -1:
            p = pics_obj.get_a_pic()

        #
        whitelisted_domains.append(p['url'])
        whitelisted_domains.append(p['media'])

        #
        normal_btn_set = list()
        normal_btn_set.append(FbButtomURL(url=p['url'], title="觀看貼文"))

        #
        new_pic_url = ins_get_pic_by_short_code(p['shortcode'])
        Element = AttachmentGenericPayloadElements(title=p["title"], subtitle=f"圖片來源:{p['url']}", image_url=new_pic_url,
                                                    default_url=p['url'], buttons=normal_btn_set,fallback_url=new_pic_url)
        pic_sets.append(Element)

    """
    # reload button
    reload_btn_set = list()
    reload_btn_set.append(FbButtomPostBack(payload=f"搜尋:{query}", title=f"搜尋更多"))

    Element = AttachmentGenericPayloadElements(title="沒有滿意的圖片？", subtitle=f"搜尋更多圖片:{query}", image_url="https://www.catster.com/wp-content/uploads/2018/04/Angry-cat-sound-and-body-language.jpg",
                                               default_url="https://www.catster.com/wp-content/uploads/2018/04/Angry-cat-sound-and-body-language.jpg", buttons=reload_btn_set)
    pic_sets.append(Element)
    """
    pic_sets_AttachmentGeneric = AttachmentGeneric(elements=pic_sets)

    if bot is not  None:
        respond = bot.add_whitelist_website(access_token=bot.access_token, whitelisted_domains=whitelisted_domains)
        print(f"respond:add_whitelist_website: {respond}")

    return pic_sets_AttachmentGeneric

