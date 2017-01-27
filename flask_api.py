from flask import Flask, request, jsonify
from urllib import request as url_request
import json
import datetime

app = Flask(__name__)

# parser = reqparse.RequestParser()
# parser.add_argument('speedGreaterThan', type=int, help='Speed of vehicle greater than')
# parser.add_argument('route_id', type=str, help='Speed of vehicle')


@app.route('/routes/')
@app.route('/routes/<speed>')
@app.route('/routes/<route_id>')
@app.route('/routes/<speed>/<route_id>/')
def getroutes(speed=None, route_id=None):
    response = url_request.urlopen('https://transitdata.phoenix.gov/api/vehiclepositions?format=json')
    string = response.read().decode('utf-8')
    parsedData = json.loads(string)

    timeStamp = parsedData['header']['timestamp']
    parsedTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')

    match = parsedData['entity']

    for n,i in enumerate(match):
        i['vehicle']['timestamp'] = datetime.datetime.fromtimestamp(i['vehicle']['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

    if speed is not None:
        match = [match[i] for i, val in enumerate(match) if val['vehicle']['position']['speed'] > int(speed)]

    if route_id is not None:
        match = [match[i] for i, val in enumerate(match) if val['vehicle']['trip']['route_id'] == route_id]

    return jsonify({'time': parsedTimeStamp, 'data': match})


@app.route('/distinctroutes')
def gerdistinctroutes():
    response = request.urlopen('https://transitdata.phoenix.gov/api/vehiclepositions?format=json')
    string = response.read().decode('utf-8')
    parsedData = json.loads(string)

    timeStamp = parsedData['header']['timestamp']
    parsedTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')

    match = parsedData['entity']

    s = set(match[i]['vehicle']['trip']['route_id'] for i, route in enumerate(match))

    return {'time': parsedTimeStamp, 'distinctRoutes': sorted(list(s))}
