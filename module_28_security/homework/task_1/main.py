from flask import Flask, jsonify, Response

app = Flask(__name__)


@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'https://go.skillbox.ru'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
    response.headers['Access-Control-Allow-Headers'] = 'X-My-Fancy-Header'
    return response


@app.route('/get_method', methods=['GET'])
def get_method_func():
    return jsonify({'GET method': 'is allowed'}), 200


@app.route('/post_method', methods=['POST'])
def post_method_func():
    return jsonify({'POST method': 'is allowed'}), 200


if __name__ == '__main__':
    app.run(port=8080, debug=True)
