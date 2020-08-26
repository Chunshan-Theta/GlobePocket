import unittest
from fb_message_bot.fb_attachment import Demo_AttachmentGeneric
from fb_message_bot.fb_button import Demo_btn_set
from fb_message_bot.fb_helper import FbHelperBot
from fb_message_bot.fb_quickreply import Demo_FbQuickReply

PAGE_ACCESS_TOKEN = "EAAluGaMwMzwBAJjhPnmpCYrgmYHTUqTDQUF8AqzByfW35TNSmLZB3ZBRvvnXF7QShTUgGE5IBIB3b9j0Ur3RxzZAUmkhPqZCw0ESZAOFh2hdfrpNlc7QyzpUt4M2Uox3hhxSggBNgFx1QSwNOok6CoCfKrMen4ZCh7LZC1rZAXgnjFN5a5x4B0cN"


class MyTestCase(unittest.TestCase):
    def test_send_templete_message(self):
        bot = FbHelperBot(PAGE_ACCESS_TOKEN)
        sender_id = "3069312713160337"
        respond = bot.send_templete_message(sender_id, Demo_AttachmentGeneric)
        print(respond)

    def test_send_button_message(self):
        bot = FbHelperBot(PAGE_ACCESS_TOKEN)
        sender_id = "3069312713160337"
        respond = bot.send_button_message(recipient_id=sender_id, text="What do you want to do next?", buttons=Demo_btn_set)
        print(respond)

    def test_send_quickreplay_message(self):
        bot = FbHelperBot(PAGE_ACCESS_TOKEN)
        sender_id = "3069312713160337"
        respond = bot.send_quickreplay_message(recipient_id=sender_id, message_obj=Demo_FbQuickReply)
        print(respond)

    def test_domain_whitelisting(self):
        bot = FbHelperBot(PAGE_ACCESS_TOKEN)
        respond = bot.add_whitelist_website(access_token=PAGE_ACCESS_TOKEN,whitelisted_domains=bot.default_domains_whitelist)
        print(respond)

    def test_image_url_message(self):
        bot = FbHelperBot(PAGE_ACCESS_TOKEN)
        respond = bot.send_image_url()
        print(respond)


    def test_image_message(self):
        sender_id = "3069312713160337"
        bot = FbHelperBot(PAGE_ACCESS_TOKEN)
        respond = bot.send_image(recipient_id=sender_id,image_path="/Users/gavinwang/simple-server-echo/fb_message_bot/test/test.png")
        print(respond)


if __name__ == '__main__':
    unittest.main()
