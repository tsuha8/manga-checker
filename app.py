from flask import Flask, request, render_template, redirect
import json
import os
import base64
import requests

app = Flask(__name__)

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ["GITHUB_REPO"]

FILE_PATH = "manga_list.json"


def get_mangas():
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(api_url, headers=headers)
    data = response.json()

    content = base64.b64decode(
        data["content"]
    ).decode("utf-8")

    return json.loads(content), data["sha"]


def save_mangas(mangas, sha, message):
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    content = json.dumps(
        mangas,
        ensure_ascii=False,
        indent=2
    )

    encoded = base64.b64encode(
        content.encode("utf-8")
    ).decode("utf-8")

    requests.put(
        api_url,
        headers=headers,
        json={
            "message": message,
            "content": encoded,
            "sha": sha
        }
    )


@app.route("/")
def index():
    mangas, sha = get_mangas()

    return render_template(
        "index.html",
        mangas=mangas
    )


@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    site = request.form["site"]
    url = request.form["url"]

    mangas, sha = get_mangas()

    mangas.append({
        "title": title,
        "site": site,
        "url": url
    })

    save_mangas(
        mangas,
        sha,
        "Add manga from web form"
    )

    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    url = request.form["url"]

    mangas, sha = get_mangas()

    mangas = [
        manga for manga in mangas
        if manga["url"] != url
    ]

    save_mangas(
        mangas,
        sha,
        "Delete manga from web form"
    )

    return redirect("/")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
