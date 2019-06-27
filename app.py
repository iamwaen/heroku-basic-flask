import json
import requests
from flask import Flask, request, abort

from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_channel_access_token = 'GCTfHrf/Sd5ewJcfnPS2mmUDaFNFgohNwoEBVrh7nSZwylTpHNmI7U0ZDnTlbxbftq/1i4ozKcFgqPNfvhqzGrGASLgJ86t8qsZMD8O/ZoBk9XiymPPGoCgJLSWhV6xzXm8qLBOC699n3PMN2HhGPwdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(line_channel_access_token)
Authorization = "Bearer {}".format(line_channel_access_token)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    body = json.loads(body)
    print (body)

    reply_token = body['events'][0]["replyToken"]
    print("reply_token: {}".format(reply_token))

    event_type = body['events'][0]['type']
    print("event_type: {}".format(event_type))

    if event_type == "message":
        message_type = body['events'][0]['message']['type']
        # print("message_type: {}".format(message_type))
        if message_type == "text":
            text = body['events'][0]['message']['text']
            print("text: {}".format(text))
            if "home" in text or "Home" in text:
                print("replying text:{}".format(text))
                reply_menu(reply_token)

    return '',200

def reply_menu(reply_token):
    response = requests.post(
        url="https://api.line.me/v2/bot/message/reply",
        headers={
            "Content-Type": "application/json",
            "Authorization": Authorization,
        },
        data=json.dumps({
            "replyToken": str(reply_token),
            "messages": [{
                            "type": "template",
                            "altText": "this is a carousel template",
                            "template": {
                                "type": "carousel",
                                "actions": [],
                                "columns": [
                                {
                                    "thumbnailImageUrl": "https://www.campusfrance.org/sites/default/files/styles/desktop_visuel_principal_page/public/Fotolia_171500112_Subscription_Monthly_M.jpg?itok=XFeTQ8UT",
                                    "title": "สภาพอากาศวันนี้",
                                    "text": "อุณหภูมิ",
                                    "actions": [
                                    {
                                        "type": "message",
                                        "label": "Detail",
                                        "text": "Detail"
                                    }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ627av9wAT7Wh-O-hn4964Wv2zH6s8ifvY4IitsPUIIISIrZD4aQ",
                                    "title": "Title",
                                    "text": "Text",
                                    "actions": [
                                    {
                                        "type": "message",
                                        "label": "Action 1",
                                        "text": "Action 1"
                                    }
                                    ]
                                }
                                ]
                            }
                        }]
        })
    )

if __name__ == "__main__":
    app.run()
