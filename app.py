from flask import Flask, request, render_template, redirect
import json
import os
import base64
import requests

app = Flask(__name__)

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ["GITHUB_REPO"]

FILE_PATH = "manga_list.json"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    site = request.form["site"]
    url = request.form["url"]

    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # 現在のmanga_list.jsonを取得
    response = requests.get(api_url, headers=headers)
    data = response.json()

    content = base64.b64decode(
        data["content"]
    ).decode("utf-8")

    mangas = json.loads(content)

    # 追加
    mangas.append({
        "title": title,
        "site": site,
        "url": url
    })

    new_content = json.dumps(
        mangas,
        ensure_ascii=False,
        indent=2
    )

    encoded = base64.b64encode(
        new_content.encode("utf-8")
    ).decode("utf-8")

    # GitHubへ保存
    requests.put(
        api_url,
        headers=headers,
        json={
            "message": "Add manga from web form",
            "content": encoded,
            "sha": data["sha"]
        }
    )

    return redirect("/")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
