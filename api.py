from flask import Flask
from flask_restful import Resource, Api, reqparse
from urllib import request
import json
import datetime

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('speedGreaterThan', type=int, help='Speed of vehicle greater than')
parser.add_argument('route_id', type=str, help='Speed of vehicle')


class Positions(Resource):
        def get(self):
            response = request.urlopen('https://transitdata.phoenix.gov/api/vehiclepositions?format=json')
            string = response.read().decode('utf-8')
            parsedData = json.loads(string)

            timeStamp = parsedData['header']['timestamp']
            parsedTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')

            match = parsedData['entity']

            for n,i in enumerate(match):
                i['vehicle']['timestamp'] = datetime.datetime.fromtimestamp(i['vehicle']['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

            args = parser.parse_args()

            if args['speedGreaterThan'] is not None:
                match = [match[i] for i, val in enumerate(match) if val['vehicle']['position']['speed'] > args['speedGreaterThan']]

            if args['route_id'] is not None:
                match = [match[i] for i, val in enumerate(match) if val['vehicle']['trip']['route_id'] == args['route_id']]

            return {'timeStamp':parsedTimeStamp, 'data':match}


class DistinctRoutes(Resource):
    def get(self):
        response = request.urlopen('https://transitdata.phoenix.gov/api/vehiclepositions?format=json')
        string = response.read().decode('utf-8')
        parsedData = json.loads(string)

        timeStamp = parsedData['header']['timestamp']
        parsedTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')

        match = parsedData['entity']

        s = set(match[i]['vehicle']['trip']['route_id'] for i, route in enumerate(match))

        return {'time': parsedTimeStamp, 'distinctRoutes': sorted(list(s))}

api.add_resource(Positions, '/routes')
api.add_resource(DistinctRoutes, '/routes/distinct')

if __name__ == '__main__':
        app.run(debug=True)