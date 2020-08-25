from flask import Flask, request, abort


## MESSENGER
PAGE_ACCESS_TOKEN="EAAluGaMwMzwBAJjhPnmpCYrgmYHTUqTDQUF8AqzByfW35TNSmLZB3ZBRvvnXF7QShTUgGE5IBIB3b9j0Ur3RxzZAUmkhPqZCw0ESZAOFh2hdfrpNlc7QyzpUt4M2Uox3hhxSggBNgFx1QSwNOok6CoCfKrMen4ZCh7LZC1rZAXgnjFN5a5x4B0cN"
MESSENGER_AUTH_TOKEN = "messenger_auth_token"
bot = FbHelperBot(PAGE_ACCESS_TOKEN)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback/messenger", methods=['GET'])
def verify():
 # Webhook verification
    if "hub.challenge" in request.args:
        return request.args["hub.challenge"], 200
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == MESSENGER_AUTH_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200



@app.route("/callback/messenger", methods=['POST'])
def webhook():

    data = request.get_json()
    #print(f"data: {data}")
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                print(f"sender_id: {sender_id}")

                messaging_text = None
                if "message" in messaging_event:
                    if "text" in messaging_event["message"]:
                        messaging_text = messaging_event["message"]["text"]
                if "postback" in messaging_event:
                    if "payload" in messaging_event["postback"]:
                        messaging_text = messaging_event["postback"]["payload"]
                if messaging_text is not None:

                    #
                    try:
                        bot.send_text_message(sender_id, f"your say: {messaging_text}")

                    except Exception as e:
                        bot.send_text_message(sender_id, f"抱歉，不了解你的指令")
                        raise e
    return "ok", 200