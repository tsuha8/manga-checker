import json
import os
import requests
from bs4 import BeautifulSoup

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage
)


CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
USER_ID = os.environ["USER_ID"]


def send_line(message):
    configuration = Configuration(
        access_token=CHANNEL_ACCESS_TOKEN
    )

    with ApiClient(configuration) as api_client:
        api = MessagingApi(api_client)

        api.push_message(
            PushMessageRequest(
                to=USER_ID,
                messages=[
                    TextMessage(text=message)
                ]
            )
        )


with open("manga_list.json", "r", encoding="utf-8") as f:
    mangas = json.load(f)


if os.path.exists("last_update.json"):
    with open("last_update.json", "r", encoding="utf-8") as f:
        old_data = json.load(f)
else:
    old_data = {}


new_data = {}
notifications = []


for manga in mangas:

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        manga["url"],
        headers=headers
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    title = soup.title.text

    print(manga["title"])
    print(title)

    new_data[manga["title"]] = title


    if manga["title"] in old_data:
        if old_data[manga["title"]] != title:
         notifications.append(
    f'◆ 最新話更新\n\n'
    f'{manga["title"]}\n'
    f'{title}\n'
    f'{manga["site"]}\n'
    f'{manga["url"]}'
)

    else:
        print("初回登録")


with open("last_update.json", "w", encoding="utf-8") as f:
    json.dump(
        new_data,
        f,
        ensure_ascii=False,
        indent=2
    )


if notifications:
    send_line(
        "\n\n".join(notifications)
    )
    print("通知送信")
else:
    print("更新なし")
