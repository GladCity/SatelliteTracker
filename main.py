from flask import Flask, request
from database import DataBase
import json
import sateliteAlgo

app = Flask(__name__)


@app.route('/check-area', methods=['POST'])
def check_area():
    jsons = json.loads(request.json)
    min_l = [1000., 0]
    max_l = [-1000., 0]
    latitude = []
    longitude = []
    for i in jsons:
        longitude.append(i[0])
        latitude.append(i[1])
        if min_l[0] > i[0]:
            min_l = i
        if max_l[0] < i[0]:
            max_l = i
    x, y = sateliteAlgo.reproject(latitude, longitude)
    area = sateliteAlgo.area_of_polygon(x, y)
    db = DataBase()
    satellites = db.get_satellites()
    out = {}
    for i in satellites:
        res = sateliteAlgo.calcRequiredTimeAndSatTrack(i.norad_id, i.photo_size, [min_l, max_l])
        if res[0] is None:
            continue
        out[i.name] = {"track": res[0], "time": res[1], "price": area * i.price, "resolution": i.details}
    return json.dumps(out)


@app.route('/get-satellite', methods=['POST'])
def get_satellite():
    db = DataBase()
    satellites = db.get_satellites()
    out = []
    for i in satellites:
        out.append(i.__dict__)
    return json.dumps(out)



if __name__ == '__main__':
    app.run(debug=True, host="192.168.8.100", port=8080)
