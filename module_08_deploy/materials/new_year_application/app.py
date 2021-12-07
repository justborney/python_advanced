import os

from flask import Flask, render_template, send_from_directory

template_folder = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory(template_folder, path)


if __name__ == "__main__":
    app.run()
