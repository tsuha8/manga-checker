from flask import Flask, request, render_template, redirect
import json

app = Flask(__name__)

FILE = "manga_list.json"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    site = request.form["site"]
    url = request.form["url"]

    with open(FILE, "r", encoding="utf-8") as f:
        mangas = json.load(f)

    mangas.append({
        "title": title,
        "site": site,
        "url": url
    })

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(
            mangas,
            f,
            ensure_ascii=False,
            indent=2
        )

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
