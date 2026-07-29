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


CHANNEL_ACCESS_TOKEN = "Z7A5WVpFdZ+ly9sS3Dvnj5WZ9nZylxci5XqPS5fBTbZXAkLfUHT/GqHHdVTQwo3ZOCDlxctg4xWEFsA9VEzHwbprvR7WdygJYcPAoTfWdwo9IUrR0z2/ZnZM3940rhmvyGLjvIpAS2ag+/BBKN4elQdB04t89/1O/w1cDnyilFU="
USER_ID = "U9042e2826eeb83cd12b9b067a1fee8ca"


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
                f'{manga["title"]}\n更新されました\n{title}'
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
        "📚 漫画更新通知\n\n" +
        "\n\n".join(notifications)
    )
    print("通知送信")
else:
    print("更新なし")