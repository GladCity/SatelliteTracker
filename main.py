from flask import Flask, request
from database import DataBase
import json

app = Flask(__name__)


@app.route('/check-area', methods=['POST'])
def check_area():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        jsons = request.json
        return jsons
    else:
        return 'Content-Type not supported!'


@app.route('/get-satellite', methods=['POST'])
def get_satellite():
    db = DataBase()
    satellites = db.get_satellites()
    out = []
    for i in satellites:
        out.append(i.__dict__)
    return json.dumps(out)


@app.route('/test', methods=['POST'])
def test():
    return json.dumps({"tema": "gay"})


@app.route('/test2', methods=['POST'])
def test2():
    return json.dumps({"tema2": "gay2"})


if __name__ == '__main__':
    app.run(debug=True, host="192.168.8.100", port=8080)
