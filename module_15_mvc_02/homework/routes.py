from flask import Flask
from models import *

app = Flask(__name__)


@app.route("/room")
def all_rooms():
    if request.args:
        return get_a_room()
    return get_all_rooms()


@app.route("/add-room", methods=["POST"])
def add_room():
    return add_new_room()


@app.route("/booking", methods=["POST"])
def book_room():
    return booking_room()


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='localhost', port=5000)
