from flask import Flask, request
from database import DataBase
import json

app = Flask(__name__)


@app.route('/add-task', methods=['POST'])
def add_task():
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


if __name__ == '__main__':
    app.run(debug=True)
