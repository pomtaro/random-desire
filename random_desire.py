
import os
import sys
import json
from datetime import datetime
import time
import requests
from flask import Flask, request
import random

app = Flask(__name__)

ACCESS_TOKEN = 'EAADmfYsX9XEBAC5gyLYVWsz9e8GjqxP6yitx9pUB4lI59p8tFvW1RLZChyvVtefw2FDC7h5Xlg0XaO3b0KZC1YPfFKIcZCHtZBmAPOsJexKOyV8pbZAmAIq9SjlPUwuUsKxzpYYO5pSxafLwzSib5S8vAsaRznEbjxJUDFAzZCQwZDZD'
VERIFY_TOKEN = 'Verify_Token_Dev'

desires = ['呼気欲求', '飲水欲求', '食物欲求', '感性欲求', '性的欲求',
           '授乳欲求', '排尿・排便欲求', '毒性回避欲求', '暑熱・寒冷回避欲求', '障害回避欲求',
           '自尊欲求', '競争欲求', '優越欲求', '攻撃欲求', '反発欲求',
           '流行欲求', '自己顕示欲求', '指導欲求', '名誉欲求', '支配欲求',
           '権力欲求', '愛情欲求', '恋愛欲求', '愉快欲求', '自由欲求',
           '自己表現欲求', '不満解消欲求', '達成欲求', '内罰欲求', '自己成長欲求',
           '持続欲求', '自己実現欲求', '知識欲求', '自己主張欲求', '批判欲求',
           '趣味欲求', '感性欲求', '理解欲求', '他社認知欲求', '好奇欲求',
           '秩序欲求', '援助欲求', '集団貢献欲求', '社会貢献欲求', '教授欲求',
           '自己認知欲求', '承認欲求', '自己開示欲求', '屈辱回避欲求', '同調欲求',
           '嫌悪回避欲求', '批判回避欲求', '服従欲求', '優位欲求', '譲歩欲求',
           '安心欲求', '気楽欲求', '挑戦欲求', '安全欲求', '拒否欲求',
           '金銭欲求', '生活安定欲求', '依存欲求', '親和欲求', '協力欲求',
           '孤立欲求', '恭順欲求', '自己規制欲求', '迷惑回避欲求']

def send_get_started():
    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "get_started": {
            "payload": "Welcome!"
        },
        "greeting": [
            {
                "locale": "default",
                "text": "マレー欲求ランダム排出"
            }
        ]
    })

    requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data)


send_get_started()


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:  # os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    data = request.get_json()
    print('***** post data *****')
    print(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]

                    if messaging_event["message"].get("text"):
                        random_desires = random.sample(desires, 3)
                        text = random_desires[0] + ', ' + random_desires[1] + ', ' + random_desires[2]
                        send_message(sender_id, text)



                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message

                    sender_id = messaging_event["sender"]["id"]

                    text = 'なんでも喋ってくれたら、ランダムに欲求を3つ答えてあげるよ。'
                    send_message(sender_id, text)



    return "ok", 200


def send_message(recipient_id, message_text):

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


def send_quick_reply(recipient_id, text, buttons):
    """
    :param recipient_id: string
    :param text: string
    :param buttons: list; string
    :return: post
    """

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    quick_replies = []

    for button in buttons:
        quick_dict = {
            "content_type": "text",
            "title": button,
            "payload": "payload: {}".format(button)
        }
        quick_replies.append(quick_dict)

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text,
            "quick_replies": quick_replies
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


def send_url_image(recipient_id, title, subtitle, url_str, image_url):
    """
    :param recipient_id: string: bot送信する相手のID
    :param title: string: タイトル
    :param subtitle: string: サブタイトル
    :param url: string: リンク先のURL
    :param url_image: string: サムネイル画像が格納されているURL
    :return: POSTリクエスト
    """

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": title,
                            "image_url": image_url,
                            "subtitle": subtitle,
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": url_str,
                                    "title": "View Website"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


def send_image(recipient_id, image_url):
    """
    画像を送るだけ
    :param recipient_id: string: bot送信する相手のID
    :param title: string: タイトル
    :param subtitle: string: サブタイトル
    :param url: string: リンク先のURL
    :param url_image: string: サムネイル画像が格納されているURL
    :return: POSTリクエスト
    """

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url,
                    "is_reusable": 'true'
                }
            }
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)



def send_buttons(recipient_id, text, buttons):
    """
    :param recipient_id: string: bot送信する相手のID
    :param title: string: タイトル
    :param subtitle: string: サブタイトル
    :param url: string: リンク先のURL
    :param url_image: string: サムネイル画像が格納されているURL
    :return: POSTリクエスト
    """

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    buttons_postback = []

    for button in buttons:
        postback_dict = {
            "type": "postback",
            "title": button,
            "payload": "postback button payload : {}".format(button)
        }
        buttons_postback.append(postback_dict)

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": buttons_postback
                }
            }
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


def send_carousel(recipient_id, titles, image_urls, subtitles, buttons_titles):
    """
    :param recipient_id: String:
    :param titles: List: String
    :param image_urls: List: String
    :param subtitles: List: String
    :param buttons_titles: List: List: String
    :return:
    """

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    elements = []
    carousel_number = len(titles)

    for num in range(carousel_number):

        buttons = []

        for button_title in buttons_titles[num]:
            button_dict = {
                "type": "postback",
                "title": button_title,
                "payload": "payload : " + button_title
            }
            buttons.append(button_dict)

        carousel_dict = {
            "title": titles[num],
            "image_url": image_urls[num],
            "subtitle": subtitles[num],
            "buttons": buttons
        }
        elements.append(carousel_dict)

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


def send_carousel_buttonless(recipient_id, titles, image_urls, subtitles):
    """
    :param recipient_id: String:
    :param titles: List: String
    :param image_urls: List: String
    :param subtitles: List: String
    :param buttons_titles: List: List: String
    :return:
    """

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    elements = []
    carousel_number = len(titles)

    for num in range(carousel_number):

        carousel_dict = {
            "title": titles[num],
            "image_url": image_urls[num],
            "subtitle": subtitles[num]
        }
        elements.append(carousel_dict)

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def send_info_validation(recipient_id):
    text = 'お疲れ様😄\n入力は以上だよ！\nこの内容で合ってるかな？\nお名前 : {}\nふりがな : {}\nメールアドレス : {}\n電話番号 : {}'.format(customer_name, customer_name_sub, customer_address, customer_number)
    buttons = ['OK👍', '修正する！']
    send_quick_reply(recipient_id, text, buttons)


def send_ok_ng_buttons(recipient_id, sender_id):
    """
    :param recipient_id: string: bot送信する相手のID
    :param title: string: タイトル
    :param subtitle: string: サブタイトル
    :param url: string: リンク先のURL
    :param url_image: string: サムネイル画像が格納されているURL
    :return: POSTリクエスト
    """

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    buttons_postback = []
    buttons = ['OK', 'NG']

    for button in buttons:
        postback_dict = {
            "type": "postback",
            "title": button,
            "payload": sender_id
        }
        buttons_postback.append(postback_dict)

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": 'OK か NG か選択して下さい。',
                    "buttons": buttons_postback
                }
            }
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


"""
登録しているIDへメッセージ
顧客からボットに送信された個人情報を、ボットから弁護士メッセンジャーへ送信する
顧客 -> ボット、ボット -> 弁護士
"""


def send_info_to_lawyer(recipient_id, customer_name, customer_name_sub, customer_address, customer_number, content):
    first_text = 'お客様からご連絡が届きました！'
    send_message(recipient_id, first_text)

    name_text = 'お名前 : ' + customer_name
    send_message(recipient_id, name_text)

    name_sub_text = 'ふりがな : ' + customer_name_sub
    send_message(recipient_id, name_sub_text)

    address_text = 'メールアドレス : ' + customer_address
    send_message(recipient_id, address_text)

    number_text = '電話番号 : ' + customer_number
    send_message(recipient_id, number_text)

    content_text = content
    send_message(recipient_id, content_text)


def send_typing_on(recipient_id):
    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": "typing_on"
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    time.sleep(0.5)


if __name__ == '__main__':
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
